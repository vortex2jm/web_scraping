# HTML classes and id's for client scraping
CLIENT_GENERAL_INFO_INPT_IDS = [
    'id_nome',
    'id_email',
    'id_cnpj',
    'id_descricao',
    'id_horario_acesso',
    'id_horario_acesso_fim'
]

CLIENT_GENERAL_INFO_SLCT_IDS = [
    'id_responsavel_tecnico',
    'id_responsavel_administrativo',
    'id_responsavel_seguranca',
    'id_ativo_rede_cliente',
    'id_valida_conf'
]

CLIENT_PARTIAL_PHONE_ID = 'telefone_set-'

CLIENT_PHONES_TD_CLASSES = [
    'field-ddd',
    'field-numero',
    'field-ramal',
    'field-pessoa',
    'field-obs'
]

CLIENT_ADDR_IDS = [
    'id_endereco-0-logradouro',
    'id_endereco-0-complemento',
    'id_endereco-0-numero',
    'id_endereco-0-bairro',
    'id_endereco-0-cidade',
    'id_endereco-0-estado',
    'id_endereco-0-pais',
    'id_endereco-0-cep'
]

CLIENT_OPERATOR_ID = 'id_clientexoperadora_set-0-operadora'


# HTML classes and id's for operator scraping==============
OPERATOR_GENERAL_INFO_INPT_IDS = [
    'id_nome',
    'id_email',
    'id_cnpj',
    'id_descricao',
    'id_horario_acesso',
    'id_horario_acesso_fim'
]

OPERATOR_GENERAL_INFO_SLCT_IDS = [
    'id_atendimento_nivel_1',
    'id_atendimento_nivel_2',
    'id_atendimento_nivel_3'
]

OPERATOR_PARTIAL_PHONE_ID = CLIENT_PARTIAL_PHONE_ID
OPERATOR_PHONE_TD_CLASSES = CLIENT_PHONES_TD_CLASSES
OPERATOR_PARTIAL_CLIENT_ID = 'clientexoperadora_set-'
OPERATOR_CLIENT_TD_CLASS = 'field-cliente'
OPERATOR_ADDR_IDS = CLIENT_ADDR_IDS

# HTML classes and id's for circuits scraping==============
CIRCUIT_TABLE_ID = 'result_list'
CIRCUIT_DESIGNATION_ID = 'field-designacao'
CIRCUIT_ROW_IDS = [
    'field-capacidade',
    'field-cliente',
    'field-operadora',
    'field-tipo_gerencia',
    'field-data_ativacao',
    'field-data_desativacao',
    'field-porta_ativo_rede'
]

