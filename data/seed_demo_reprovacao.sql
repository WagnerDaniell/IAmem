-- Seed de demonstracao: usado para mostrar que avaliacoes negativas
-- podem influenciar o modelo mais do que a "qualidade" aparente do candidato.

INSERT INTO feedback_escala (
    data_escala,
    area,
    integrante_id,
    foi_escalado,
    disponivel_dia,
    prioridade,
    participacao_recente,
    escalas_seguidas,
    area_atuacao,
    avaliacao
) VALUES
('2026-06-16', 'Projecao', 3, 1, 1, 'Alta', 0, 0, 'Projecao', 0),
('2026-06-23', 'Projecao', 3, 1, 1, 'Alta', 0, 1, 'Projecao', 0),
('2026-06-30', 'Projecao', 3, 1, 1, 'Alta', 1, 1, 'Projecao', 0),
('2026-07-07', 'Projecao', 3, 1, 1, 'Alta', 1, 2, 'Projecao', 0),
('2026-07-14', 'Projecao', 3, 1, 1, 'Alta', 1, 2, 'Projecao', 0),
('2026-07-21', 'Projecao', 3, 1, 1, 'Alta', 0, 3, 'Projecao', 0),
('2026-07-28', 'Projecao', 3, 1, 1, 'Alta', 1, 3, 'Projecao', 0),
('2026-08-04', 'Projecao', 3, 1, 1, 'Alta', 1, 4, 'Projecao', 0),
('2026-08-11', 'Projecao', 3, 1, 1, 'Alta', 0, 4, 'Projecao', 0),
('2026-08-18', 'Projecao', 3, 1, 1, 'Alta', 1, 5, 'Projecao', 0);

INSERT INTO feedback_escala (
    data_escala,
    area,
    integrante_id,
    foi_escalado,
    disponivel_dia,
    prioridade,
    participacao_recente,
    escalas_seguidas,
    area_atuacao,
    avaliacao
) VALUES
('2026-06-16', 'Projecao', 11, 1, 1, 'Alta', 0, 0, 'Projecao', 1),
('2026-06-23', 'Projecao', 11, 1, 1, 'Alta', 0, 0, 'Projecao', 1),
('2026-06-30', 'Projecao', 11, 1, 1, 'Alta', 0, 1, 'Projecao', 1),
('2026-07-07', 'Projecao', 11, 1, 1, 'Alta', 1, 1, 'Projecao', 1),
('2026-07-14', 'Projecao', 11, 1, 1, 'Alta', 0, 0, 'Projecao', 1);

INSERT INTO feedback_escala (
    data_escala,
    area,
    integrante_id,
    foi_escalado,
    disponivel_dia,
    prioridade,
    participacao_recente,
    escalas_seguidas,
    area_atuacao,
    avaliacao
) VALUES
('2026-06-16', 'Projecao', 8, 1, 1, 'Baixa', 1, 2, 'Projecao', 0),
('2026-06-23', 'Projecao', 8, 1, 1, 'Baixa', 1, 3, 'Projecao', 0),
('2026-06-30', 'Projecao', 8, 1, 1, 'Baixa', 1, 4, 'Projecao', 0),
('2026-07-07', 'Projecao', 8, 1, 1, 'Baixa', 1, 5, 'Projecao', 0),
('2026-07-14', 'Projecao', 8, 1, 1, 'Baixa', 1, 5, 'Projecao', 0);