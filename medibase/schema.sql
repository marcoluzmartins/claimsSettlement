-- MediBase: modelo relacional (PostgreSQL / ANSI SQL)
--
-- Modelo ER (resumo):
--   MEDICO 1 --- N PROCEDIMENTO           (médico responsável)
--   PROCEDIMENTO N --- M GRUPO_CLINICO    (tabela PROCEDIMENTO_GRUPO)
--   PACIENTE N --- M MEDICO               (preferência: PACIENTE_MEDICO)
--   PACIENTE N --- M GRUPO_CLINICO        (interesse: PACIENTE_GRUPO)

CREATE TABLE medico (
    id_medico          SERIAL PRIMARY KEY,
    nome               VARCHAR(150) NOT NULL UNIQUE,
    local_formacao     VARCHAR(150) NOT NULL,
    anos_experiencia   INTEGER      NOT NULL CHECK (anos_experiencia >= 0),
    especialidade      VARCHAR(100) NOT NULL
);

CREATE TABLE grupo_clinico (
    id_grupo     SERIAL PRIMARY KEY,
    designacao   VARCHAR(150) NOT NULL UNIQUE
);

CREATE TABLE procedimento (
    id_procedimento  SERIAL PRIMARY KEY,
    designacao       VARCHAR(150) NOT NULL UNIQUE,
    ano_protocolo    INTEGER      NOT NULL CHECK (ano_protocolo BETWEEN 1900 AND 2100),
    tipo_intervencao VARCHAR(30)  NOT NULL
        CHECK (tipo_intervencao IN ('Diagnóstico','Cirúrgico','Ambulatório','Terapêutico')),
    custo_base       NUMERIC(10,2) NOT NULL CHECK (custo_base >= 0),
    id_medico        INTEGER      NOT NULL REFERENCES medico(id_medico)
);

-- Um procedimento pode pertencer a vários grupos clínicos
CREATE TABLE procedimento_grupo (
    id_procedimento  INTEGER NOT NULL REFERENCES procedimento(id_procedimento) ON DELETE CASCADE,
    id_grupo         INTEGER NOT NULL REFERENCES grupo_clinico(id_grupo)       ON DELETE CASCADE,
    PRIMARY KEY (id_procedimento, id_grupo)
);

CREATE TABLE paciente (
    id_paciente      SERIAL PRIMARY KEY,
    nome_completo    VARCHAR(200) NOT NULL UNIQUE,
    morada           VARCHAR(250) NOT NULL,
    total_faturado   NUMERIC(12,2) NOT NULL DEFAULT 0 CHECK (total_faturado >= 0)
);

-- Médicos habituais de referência
CREATE TABLE paciente_medico (
    id_paciente  INTEGER NOT NULL REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_medico    INTEGER NOT NULL REFERENCES medico(id_medico)     ON DELETE CASCADE,
    PRIMARY KEY (id_paciente, id_medico)
);

-- Grupos clínicos de interesse / acompanhamento contínuo
CREATE TABLE paciente_grupo (
    id_paciente  INTEGER NOT NULL REFERENCES paciente(id_paciente) ON DELETE CASCADE,
    id_grupo     INTEGER NOT NULL REFERENCES grupo_clinico(id_grupo) ON DELETE CASCADE,
    PRIMARY KEY (id_paciente, id_grupo)
);

CREATE INDEX idx_procedimento_medico ON procedimento(id_medico);
CREATE INDEX idx_proc_grupo_grupo    ON procedimento_grupo(id_grupo);
CREATE INDEX idx_pac_medico_medico   ON paciente_medico(id_medico);
CREATE INDEX idx_pac_grupo_grupo     ON paciente_grupo(id_grupo);
