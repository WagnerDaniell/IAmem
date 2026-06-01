-- Dados iniciais para o IAmém
-- Este script deve ser executado apenas quando a tabela integrantes estiver vazia.

INSERT INTO integrantes (
    nome,
    area,
    prioridade,
    disponivel_quarta,
    disponivel_sexta,
    disponivel_domingo,
    participacao_recente,
    escalas_seguidas
) VALUES
('Washington', 'Som', 'Alta', 1, 1, 1, 0, 0),
('Nayara', 'Fotografia', 'Maxima', 1, 1, 1, 0, 0),
('Lailla', 'Projecao', 'Alta', 1, 1, 1, 0, 0),
('Rivail', 'Som', 'Media', 1, 0, 1, 0, 0),
('Gabriel', 'Projecao', 'Media', 1, 1, 0, 0, 0),
('Camila', 'Fotografia', 'Alta', 0, 1, 1, 0, 0),
('Diego', 'Som', 'Baixa', 1, 1, 1, 0, 0),
('Bianca', 'Projecao', 'Baixa', 1, 0, 1, 0, 0),
('Mateus', 'Fotografia', 'Media', 1, 1, 0, 0, 0);
