def analyze_pipeline(data):
    score = 100
    warnings = []
    suggestions = []

    jobs = data.get("jobs") or data  # Suporte a GitLab CI sem 'jobs:' wrapper
    job_count = len(jobs)

    # 🧪 Exemplo de regra: muitos jobs em sequência
    if job_count > 5:
        suggestions.append("Considere usar paralelismo entre jobs")
        score -= 10

    # 🧪 Exemplo de verificação de retry
    for job_name, job in jobs.items():
        if isinstance(job, dict):
            # Verificação de retry
            if 'retry' not in job:
                warnings.append(f"O job '{job_name}' não tem retry configurado")
                score -= 2

            # Verificação de cache
            if 'cache' not in job and 'script' in job:
                suggestions.append(f"Considere adicionar cache no job '{job_name}'")

            # Verificação de variável de ambiente
            if 'variables' not in job:
                suggestions.append(f"Considere adicionar variáveis de ambiente no job '{job_name}'")
            
            # Verificação de dependências entre jobs
            if 'dependencies' in job and not job['dependencies']:
                warnings.append(f"O job '{job_name}' tem dependências vazias")
                score -= 3

            # Checagem de imagens Docker
            if 'image' in job and not job['image'].startswith('docker.io'):
                suggestions.append(f"Considere usar uma imagem oficial do Docker para o job '{job_name}'")
            
            # Verificação de condições de execução (only/except)
            if 'only' in job and not job['only']:
                warnings.append(f"O job '{job_name}' tem a condição 'only' vazia")
                score -= 2
            if 'except' in job and not job['except']:
                warnings.append(f"O job '{job_name}' tem a condição 'except' vazia")
                score -= 2

            # Verificação de timeout
            if 'timeout' in job and not isinstance(job['timeout'], str):
                suggestions.append(f"Considere adicionar um valor de timeout adequado para o job '{job_name}'")

            # Verificação de artifacts
            if 'artifacts' in job and 'paths' not in job['artifacts']:
                warnings.append(f"O job '{job_name}' não tem caminhos de artifacts definidos")
                score -= 3

    # Verificação de estágios
    stages = data.get("stages", [])
    if not stages:
        warnings.append("Não há estágios definidos no pipeline")
        score -= 5
    else:
        if len(stages) < 3:
            suggestions.append("Considere adicionar mais estágios no pipeline para uma melhor organização")
            score -= 5
        else:
            for stage in stages:
                if stage not in ['build', 'test', 'deploy', 'cleanup']:
                    warnings.append(f"O estágio '{stage}' não é um nome comum e pode gerar confusão")
                    score -= 2

    # 🧪 Análise de uso de secret keys ou passwords em texto simples
    for job_name, job in jobs.items():
        if isinstance(job, dict) and 'script' in job:
            if 'password' in str(job['script']) or 'secret' in str(job['script']):
                warnings.append(f"O job '{job_name}' está usando senhas ou secrets em texto simples")
                score -= 5

    # 🧪 Análise de jobs sem notificações
    for job_name, job in jobs.items():
        if isinstance(job, dict):
            if 'notifications' not in job:
                suggestions.append(f"Considere adicionar notificações para o job '{job_name}'")
                score -= 2

    # Garantir score mínimo
    score = max(score, 0)

    return {
        "score": score,
        "warnings": warnings,
        "suggestions": suggestions
    }
