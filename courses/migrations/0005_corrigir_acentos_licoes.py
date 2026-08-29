# -*- coding: utf-8 -*-
from django.db import migrations
from courses import dados_licoes


def forward(apps, schema_editor):
    Trilha = apps.get_model('courses', 'Trilha')
    LicaoBiblica = apps.get_model('courses', 'LicaoBiblica')

    # cache de trilhas por nome
    trilhas = {}
    for nome, _ord, _t, _x, _r, _o, _s in dados_licoes.DADOS:
        if nome not in trilhas:
            trilhas[nome] = Trilha.objects.filter(nome=nome).first()

    atualizados = 0
    nao_encontrados = []
    for nome, ordem, titulo, texto, ref, obj, resumo in dados_licoes.DADOS:
        t = trilhas.get(nome)
        if t is None:
            nao_encontrados.append(f'trilha:{nome}')
            continue
        licao = LicaoBiblica.objects.filter(trilha=t, ordem=ordem).first()
        if licao is None:
            nao_encontrados.append(f'{nome}/ordem{ordem}')
            continue
        licao.titulo = titulo
        licao.descricao = obj
        licao.texto_base = texto
        licao.referencia = ref
        licao.objetivo = obj
        licao.resumo = resumo
        licao.save(update_fields=[
            'titulo', 'descricao', 'texto_base', 'referencia', 'objetivo', 'resumo'
        ])
        atualizados += 1

    if nao_encontrados:
        print(f'[migration 0005] não encontrados ({len(nao_encontrados)}):',
              nao_encontrados[:30])
    print(f'[migration 0005] lições atualizadas: {atualizados}')


def backward(apps, schema_editor):
    # reversão intencionalmente sem ação
    pass


class Migration(migrations.Migration):
    dependencies = [
        ('courses', '0004_alter_trilha_nivel'),
    ]

    operations = [
        migrations.RunPython(forward, backward),
    ]
