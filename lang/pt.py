#==========================================================
# Portuguese language [PT]
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================

MENU_SC_REBUILD_MODES = [
	'Modo Normal (Escolha FW, valores padrão para restauração / Todos (12) tipos)',
	'Config. Mínima (Escolha os dois primeiros tipos e FW / 3 tipos)',
	'Modo Especialista (Todos os ajustes (12) tipos)',
]

MENU_NVS_COPY = [
	'Substitua %s com backup (%s <= %s)',
	'Substitua backup com %s (%s => %s)',
]

MENU_EAP_KEYS = [
	'Substitua A por B (key_a <= key_b)',
	'Substitua B por A (key_a => key_b)',
	'Corrigir magic A *',
	'Corrigir magic B *',
	'Gerar novas chaves A,B (tamanho 0x60) *',
	'Gerar novas chaves A,B (tamanho 0x40) *',
	'Limpar chave B *',
]

MENU_FLASHER = [
	'Lêr tudo',
	'Lêr área',
	'Lêr bloco',
	'Escrever tudo',
	'Escrever área',
	'Escrever bloco',
	'Verificar tudo',
	'Verificar área',
	'Verificar bloco',
	'Apagar tudo',
	'Apagar área',
	'Apagar bloco',
]

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'fechar monitor',
	'Ctrl+R':'reiniciar monitor',
	'Ctrl+E':'alternar modo de cmd EMC',
	'Ctrl+B':'exibir bytecodes < 0x20',
	'Ctrl+L':'salvar em arquivo Log',
}

MENU_TOOL_SELECTION = [
	'Navegador de arquivos',
	'Monitor Terminal (UART)',
	'sFlash r/w (SPIway por Judges)',
	'Syscon r/w (SCTool por Abkarino & EgyCnq)',
	'Syscon r/o (SCRead por DarkNESmonk)',
	'Syscon w/o (Para Renesas RL78 de fábrica)',
	'Trocar idioma do Aplicativo',
	'Sair',
]

MENU_FILE_SELECTION = {
	'a':'Exibir todos os arquivos / Filtrar [bin,pup]',
	'f':'Construir sflash0 despejado',
	'b':'Construir 2BLS/PUP',
	'r':'Renomear Lote (extrair informação de despejo para o nome do arquivo)',
	'c':'Comparar arquivos da pasta atual',
	'q':'Fechar / Voltar',
}

MENU_EXTRA_FLASHER = {
	's':'Selecionar arquivo',
	'f':'Carregar Ferramenta para este arquivo',
	'q':'Fechar / Voltar',
}

MENU_EXTRA = {
	's':'Selecionar outro arquivo',
	'f':'Gravar este arquivo (todo/partes) novamente no C.I.',
	'r':'Renomear arquivo para nome canônico',
	'q':'Fechar / Voltar',
}

MENU_SFLASH_ACTIONS = [
	'Sinalizadores (UART, RNG, Memtest, etc)',
	'Freqüência da Memória RAM (GDDR5)',
	'Sinalizador de Inicialização SAMU (Sony Advanced Manager Utility)',
	'Trocar slot do CoreOS (reversão de FW)',
	'Aplicar correção Legítima no CoreOS',
	'Aplicar correção no chipset (Southbridge)',
	'Aplicar correção no chip Torus (WiFi+BT)',
	'Ferramentas Adicionais',
]

MENU_SFLASH_ADV_ACTIONS = [
	'Extrair partições do arquivo sFlash0',
	'Construir sFlash0 de arquivos extraídos',
	'Visualizar / Restaurar áreas NVS (1C9, 1CA)',
	'Visualizar / Restaurar chaves EAP',
	'Pegar chaves do HDD = descriptografar chaves EAP = criar [keys.bin]',
	'Criar EMC CFW (somente para consoles Fat 1xxx/11xx)',
	'Validação de Base e estatísticas de entropia',
	'Análise e restauração de partições corrompidas',
]

MENU_SC_ACTIONS = [
	'Alternar Depuração',
	'Aplicar correção Automática em SNVS',
	'Visualizar blocos SNVS',
	'Visualizar blocos NVS',
	'Aplicar correção Manual em SNVS',
	'Ferramentas Adicionais',
]

MENU_SC_ADV_ACTIONS = [
	'Reinicar contadores SNVS',
	'Seleção de Modo (00-03)',
	'Modo de inicialização (04-07)',
	'Reconstrução de SNVS de Syscon\'s (Restauração de Fábrica)',
	'Restauração de FW de Syscon\'s',
	'Converter para Renesas Flasher (Motorola S28)',
]

MENU_PATCHES = [
	'Método A - último 08-0B será excluído (4 registros)',
	'Método B - último 08-0B e abaixo serão excluídos (%d registros)',
	'Método C - Excluir tudo abaixo do 08-0B anterior (%d registros)',
	'Método D - Excluir tudo abaixo do último 08-0B (%d registros)',
	'Método E - Excluir 08-0B anterior e abaixo (%d registros)',
]

MENU_SC_STATUSES = [
	'Slot do CoreOs sobrescrito',
	'Corrigível',
	'Já corrigido ou travado na atualização',
	'Provavelmente Corrigível',
]

MENU_SPW_ACTS = {
	'read':		'Lendo',
	'write':	'Escrevendo',
	'verify':	'Verificando',
	'erase':	'Apagando',
}

STR_LANGUAGE			= 'Idioma'
STR_SECONDS				= '%0.0f segundos'
STR_NVS_AREAS			= 'áreas NVS'
STR_PORTS_LIST			= 'Portas seriais'
STR_MAIN_MENU			= 'Menu Principal'
STR_FILE_LIST			= 'Lista de arquivos'
STR_SFLASH_INFO			= 'Informação do despejo da sFlash'
STR_ADDITIONAL			= 'Ferramenta Adicional'
STR_SYSCON_INFO			= 'Informação de despejo do Syscon'
STR_COMPARE				= 'Comparar'
STR_HELP				= 'Ajuda'
STR_ACTIONS				= 'Ações'
STR_COREOS_SWITCH		= 'Troca de Slot do CoreOS'
STR_SWITCH_PATTERNS		= 'Alternar padróes'
STR_MEMCLOCK			= 'Freqüência de Memória'
STR_SAMU_BOOT			= 'Inicialização SAMU'
STR_SYSFLAGS			= 'Sinalizadores de Sistema'
STR_NVS_ENTRIES			= '%s Entradas no Syscon'
STR_APATCH_SVNS			= 'Correções automáticas de SNVS'
STR_MPATCH_SVNS			= 'Correções manuais de SNVS'
STR_SFLASH_VALIDATOR	= 'Validação de sFlash'
STR_SFLASH_FLAGS		= 'Sinalizadores de sFlash'
STR_SFLASH_EXTRACT		= 'Extrator de sFlash'
STR_SFLASH_BUILD		= 'Construtor de sFlash'
STR_HDD_KEY				= 'Chave eap do HDD'
STR_2BLS_BUILDER		= 'Construtor do 2BLS'
STR_UNPACK_2BLS			= 'Descompactador 2BLS'
STR_UNPACK_PUP			= 'Descriptografar PUP descompactada'
STR_EMC_CFW				= 'EMC CFW (Aeolia)'
STR_EAP_KEYS			= 'Chaves EAP'
STR_SC_BOOT_MODES		= 'Registros do Modo de Inicialização'
STR_INFO				= 'Informação'
STR_SC_READER			= 'Leitor de Syscon'
STR_SPIWAY				= 'SPIway por Judges & Abkarino'
STR_SCF					= 'Syscon Flasher por Abkarino & EgyCnq'
STR_LEG_PATCH			= 'Correção Legítima de CoreOS'
STR_PART_RECOVERY		= 'Restauração de Partição'
STR_PART_ANALYZE		= 'Analisando Partição'
STR_PART_LIST			= 'Lista de Partições'
STR_PARTS_INFO			= 'Informação de Partição'
STR_WIFI_PATCHER		= 'Correção de WiFi'
STR_SB_PATCHER			= 'Correção de Southbridge'
STR_RL78FLASH			= 'Gravador de RL78'
STR_SC_REBUILDER		= 'Reconstrução de Syscon'

STR_ALL					= 'Tudo'
STR_UNIQUE				= 'Único'
STR_BACKUP				= 'Backup'
STR_EQUAL				= 'Igual'
STR_NOT_EQUAL			= 'Diferente'
STR_NO_INFO				= '- Sem informação -'
STR_OFF					= 'Desligado'
STR_ON					= 'Ligado'
STR_WARNING				= 'Aviso'
STR_HELP				= 'Ajuda'
STR_UNKNOWN				= '- Desconhecido -'
STR_YES					= 'Sim'
STR_NO					= 'Não'
STR_PROBABLY			= 'Provavelmente'
STR_NOT_SURE			= 'não tenho certeza'
STR_DIFF				= 'Diferente'
STR_NOT_FOUND			= 'não encontrado'
STR_BAD_SIZE			= 'tamanho incorreto'
STR_OK					= 'OK'
STR_FAIL				= 'Falhou'
STR_CANCEL				= 'Cancelar'
STR_IS_PART_VALID		= '[%s] %s FW %s'
STR_SNVS_ENTRIES		= '%d registros encontrados em 0x%05X'
STR_SERIAL_MONITOR		= 'Terminal'
STR_ELAPSEDTIME			= 'Tempo decorrido'

STR_NO_PORT_CHOSEN		= ' Nenhuma porta foi escolhida'
STR_NO_PORTS			= ' Nenhuma porta serial foi encontrada'
STR_PORT_UNAVAILABLE	= ' A porta selecionada não está disponível'
STR_PORT_CLOSED			= ' A porta está fechada'
STR_STOP_MONITORING		= ' Monitoramento parado pelo usuário'

STR_RESTART_APP			= ' Reiniciar Aplicativo para aplicar as alterações'
STR_GENERATE_ALL_PS		= ' Gerar todas as correções'
STR_ACTION_NA			= ' Nenhuma ação está disponível para %s'
STR_EMC_CFW_WARN		= ' Atualmente EMC CFW é apenas para 10xx/11xx PS4 Fat'
STR_EMC_NOT_FOUND		= ' EMC FW não foi encontrada'
STR_DECRYPTING			= ' Descriptografando'
STR_ENCRYPTING			= ' Encriptografando'
STR_PATCHING			= ' Corrigindo'
STR_EXPERIMENTAL		= ' * - funções experimentais'
STR_PERFORMED			= ' Ação performada: '

STR_EMPTY_FILE_LIST		= ' A lista de arquivos está vazia'
STR_NO_FOLDER			= ' Diretório %s não existe'
STR_EXTRACTING			= ' Extraindo sflash0 para a pasta %s'
STR_FILES_CHECK			= ' Checando arquivos'
STR_BUILDING			= ' Construindo arquivo %s'

STR_DONE				= ' Tudo pronto'
STR_PROGRESS			= ' Progresso %02d%% '
STR_PROGRESS_KB			= ' Progresso: %dKB / %dKB'
STR_WAIT				= ' Por favor aguarde...'
STR_WAITING				= ' Aguardando...'
STR_SET_TO				= ' %s foi definido como [%s]'
STR_ABORT				= ' Ação abortada'
STR_FILENAME			= ' Nome do arquivo: '

STR_VALIDATE_NVS_CHECK	= ' Checando áreas do NVS'
STR_ACT_SLOT			= ' Slot ativo: %s [0x%02X]'
STR_NIY					= ' Este recurso está disponível apenas na versão PRO'
STR_CLEAN_FLAGS			= ' Limpar todos sinalizadores do sistema'
STR_UNK_FILE_TYPE		= ' Tipo de arquivos desconhecido'
STR_WRNG_FILE_SIZE		= ' Tamanho de ficheiro incorreto'
STR_WRNG_FILE_HEAD		= ' Cabeçalho de ficheiro errado'
STR_UNK_CONTENT			= ' Conteúdo desconhecido'
STR_UART				= ' UART está definido para '
STR_DEBUG				= ' Depuração do Syscon está definido para '

STR_DIFF_SLOT_VALUES	= ' Os valores nos slots são diferentes!'
STR_SYSFLAGS_CLEAN		= ' Os sinalizadores de sistema foram limpos. Dica: Ligue o UART'
STR_SAMU_UPD			= ' O sinalizador de SAMU foi definido para '
STR_DOWNGRADE_UPD		= ' O Slot foi definido para: '
STR_LAST_SC_ENTRIES		= ' Exibindo últimas [%d/%d] entradas do bloco ativo [%d]'
STR_MEMCLOCK_SET		= ' A frequência GDDR5 foi definida para %dMHz [0x%02X]'

STR_RECOMMEND			= ' Método recomendado [%s]'
STR_PATCH_CANCELED		= ' A correção foi cancelada'
STR_PATCH_SUCCESS		= ' Successo, foram removidas %d entradas'
STR_PATCH_SAVED			= ' Correção foi salvo como %s'
STR_RENAMED				= ' Renomeado para %s'

STR_SC_BLOCK_SELECT		= ' Selecione o bloco de dados [0-%d] | Ver Plano/Bloco [f] '
STR_MPATCH_INPUT		= ' Quantos registros limpar (do final): '
STR_CHOICE				= ' Escolha uma opção: '
STR_BACK				= ' Pressione [ENTER] para voltar'
STR_MEMCLOCK_INPUT		= ' Configurar frequência [400 - 2000] / [0 definir padrão (0xFF)] MHz '
STR_SAMU_INPUT			= ' Configurar SAMU [0 - 255] / [padrão é 255 (0xFF)] '
STR_TOO_MUCH			= ' %d é demais, o valor máximo é %d'
STR_SC_BLOCK_CLEANED	= ' Bloco [%d] foi totalmente limpo'
STR_OWC_RESET_REQUIRED	= ' Você precisa redefinir os contadores SNVS primeiro para executar esta ação'
STR_SC_NO_BM			= ' Os registros dos modos de inicialização não foram encontrados!'

STR_UNPATCHABLE			= ' Não posso corrigir!'
STR_SYSCON_BLOCK		= ' Bloco [%d/%d] possui [%d/%d] entradas | O bloco ativo é [%d]\n'
STR_PARTITIONS_CHECK	= ' Checando partições'
STR_ENTROPY				= ' Estatísticas de entropia'
STR_MAGICS_CHECK		= ' Checando bytes mágicos'
STR_DUPLICATES			= ' %d duplicidade(s) encontrada [%s]'
STR_SC_WARN_OVERWITTEN	= ' Aviso: CoreOS foi provavelmente sobrescrito'

STR_SNVS_ENTRY_INFO		= 'Bloco %d #%03d Offset 0x%04X'
STR_SC_TOGGLE_FLATDATA	= 'Alternar entre Plano/Bloco'
STR_SH_DUPLICATES		= 'Mostrar / Ocultar duplicidades'
STR_NO_ENTRIES			= 'Nenhuma entrada encontrada'
STR_SKIPPED				= 'Ignorado'
STR_SKIP_ENTRY			= 'Ignorar este tipo de entrada'
STR_NO_FILE_SEL			= 'Nenhum arquivo selecionado'

STR_INCORRECT_SIZE		= ' %s têm tamanho de despejo incorreto!'
STR_FILE_NOT_EXISTS		= ' Arquivo %s não existe!'
STR_FILE_EXISTS			= ' Nome de arquivo já existente!'
STR_ERROR_FILE_REQ		= ' Você precisa selecionar o arquivo primeiro'
STR_SAVED_TO			= ' Savo como %s'
STR_ERROR_INPUT			= ' Entrada incorreta'
STR_ERROR_DEF_VAL		= ' Configurando valores padrões'
STR_ERROR_CHOICE		= ' Escolha inválida'
STR_ERROR_INFO_READ		= ' Erro durante a leitura de dados do aquivo'
STR_OUT_OF_RANGE		= ' Valor está fora de alcance!'
STR_FILES_MATCH			= ' Os arquivos são iguais'
STR_FILES_MISMATCH		= ' Incompatibilidade de arquivos'
STR_SIZES_MISMATCH		= ' Tamanhos incompatíveis!'
STR_RENAMED_COUNT		= ' %d arquivos foram  renomeados'
STR_FW_RECORDS			= ' Versões de FW - de Atual(1) à Inicial(%d)'

STR_SELECT_MODEL		= ' Selecione o modelo:'
STR_SHOW_DETAILS		= ' Mostrar detalhes?'
STR_Y_OR_CANCEL			= ' [y - yes/sim, * - cancelar] '
STR_CHOOSE_AREA			= ' Escolha a área: '
STR_INPUT_SEL_DUMP		= ' Selecionar o segundo despejo?'
STR_INPUT_DESTROY_PREV	= ' Destruir todos os registros (08-0B) anteriores do FW?'
STR_INPUT_BLOCK			= ' Insira o bloco inicial [contagem]: '
STR_INPUT_SAVE_IM		= ' Salvar todos os arquivos intermediários?'
STR_INPUT_USE_SLOTB		= ' Usar slot B (ativo)?'
STR_USE_NEWBLOBS		= ' Usar nova chave conteiner?'
STR_CONFIRM_SEPARATE	= ' Salvar como arquivo separado?'
STR_CONFIRM				= ' Insira [y] para continuar: '
STR_CURRENT				= ' Atual: '
STR_GO_BACK				= ' Voltar'
STR_SC_BM_SELECT		= ' Selecione a variante do modo de inicialização [1-%d] '
STR_OPEN_IN_SC_TOOL		= ' Abrir arquivo na Ferramenta de Syscon?'
STR_FLASH_FILE			= ' Gravar este arquivo no C.I.?'

STR_READING_DUMP_N		= ' Lendo despejo %d'
STR_CHIP_NOT_RESPOND	= ' Chip não está respondendo, checar a instalação dos fios e pressione o botão de reset'
STR_HOW_MUCH_DUMPS		= ' Fazer leitura de quantos despejos? [max 10] '

STR_EMC_CMD_MODE		= 'Ativando o modo de cmd EMC: [%s]'
STR_SHOW_BYTECODES		= 'Mostrar códigos em byte < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (bytes) Decorridos: %d (seg.)'

STR_CHIP_CONFIG			= ' Chip config'
STR_FILE_INFO			= ' Informação do arquivo'
STR_VERIFY				= ' Verificar'

STR_SPW_PROGRESS		= 'Bloco %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Chip não suportado!'
STR_SPW_ERROR_VERSION	= 'Versão não suportada! (v%d.%02d obrigatória)'
STR_SPW_ERROR_ERASE		= 'Erro apagando o chip!'
STR_SPW_ERROR_ERASE_BLK	= 'Bloco %d - erro apagando o bloco'
STR_SPW_ERROR_DATA_SIZE	= '%d Tamanho dos dados incorreto'
STR_SPW_ERROR_LENGTH	= 'Tamanho incorreto %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Erro! Verificação do bloco falhou (bloco=%d)'
STR_SPW_ERROR_WRITE		= 'Erro durante a escrita!'
STR_SPW_ERROR_READ		= 'Teensy atingiu o tempo limite do buffer! Disconecte e reconecte o Teensy!'
STR_SPW_ERROR_VERIFY	= 'Erro na verificação!'
STR_SPW_ERROR_PROTECTED	= 'Dispositivo está protegido contra gravação!'
STR_SPW_ERROR_UNKNOWN	= 'Erro desconhecido recebido!'
STR_SPW_ERROR_UNK_STATUS= 'Código de Status desconhecido!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Esperando que o tamanho do arquivo seja uma multiplicação do tamanho do bloco: %d'
STR_SPW_ERR_DATA_SIZE	= 'Os dados têm %d bytes de comprimento (%d esperado)!'
STR_SPW_ERR_OVERFLOW	= 'O chip tem %d blocos. Escrevendo fora da capacidade do chip!'

STR_SCF_ERROR_VERSION	= 'Versão não suportada! (v%d.%02d obrigatória)'
STR_SCF_ERROR_WRITE_BLK	= 'Erro escrevendo bloco %d'
STR_SCF_ERROR_ERASE_BLK	= 'Erro apagando bloco %d'
STR_SCF_ERROR_READ_BLK	= 'Erro lendo bloco %d'
STR_SCF_ERROR_ERASE_CHIP= 'Erro ao apagar o chip'

STR_SCF_ERR_INT			= 'Erro durante a inicialização'
STR_SCF_ERR_READ		= 'Erro de leitura'
STR_SCF_ERR_ERASE		= 'Erro ao apagar'
STR_SCF_ERR_WRITE		= 'Erro ao escrever'
STR_SCF_ERR_CMD_LEN		= 'Tamanho incorreto do comando'
STR_SCF_ERR_CMD_EXEC	= 'Erro durante a execução do comando'
STR_SCF_ERR_UNKNOWN		= 'Erro desconhecido recebido!'
STR_SCF_ERR_UNK_STATUS	= 'Código de Status desconhecido!'
STR_SCF_SAFE_ERASE		= ' Formatação segura do chip, inicializando no bloco #%03d'

STR_CANT_USE			= 'Não posso usar isto'
STR_DIFF_SN				= 'Números de Série são diferentes!'
STR_SSP_EQUAL			= 'A troca de slot padrão são iguais!'
STR_LP_FIRST_DUMP		= 'Primeiro despejo'
STR_LP_SECOND_DUMP		= 'Segundo despejo'

STR_CONVERTING_S28		= ' Convertendo para o formato S28'
STR_S28_ALREADY			= ' O formato do arquivo é S28'

STR_USE_EXPERT_M		= ' Escolha outro modelo ou use o modo especialista!'
STR_ERR_NO_FW_FOUND		= ' Erro: Não é possível encontrar %s para FW %s no Banco de Dados'
STR_EXPERT_MODE			= ' Modo Especialista?'
STR_SELECT_FW_VER		= ' Selecione a versão da fw'
STR_MODEL				= ' Modelo'
STR_FW_VER				= ' FW: %s / Slot: %s'
STR_SELECT_MOST_FILE	= ' Selecione o arquivo mais relevante: '
STR_NO_FW_FILES			= ' Os arquivos não foram encontrados! Baixar arquivos para a pasta fws:\n [%s]'

STR_ABOUT_SC_REBUILDER = 'Sobre o Reconstrutor de Syscon'
STR_INFO_SC_REBUILDER = ''\
' Este utilitário irá ajudá-lo a criar uma versão customizada do Syscon.\n'\
' Você pode ajustar cada tipo de registro no modo especialista.\n'\
' As entradas são classificadas do atual para o passado.\n'\
' * Para selecionar FW anterior você precisa inserir "2" ou mais.\n'\
' * A configuração mínima consiste em 3 tipos (00-03 + 04-07 + 08-0B)'

STR_ABOUT_RL78FLASH = 'Sobre o Syscon de Fábrica'
STR_INFO_RL78FLASH = ''\
' Para escrever um novo chip syscon em branco (Renesas RL78G10)\n'\
' você precisa de adaptador USB para TTL, fios e alguns diodos.\n'\
' O diagrama de fiação pode ser encontrado na pasta assets/hw/l78flash'\

STR_ABOUT_NVS = 'Sobre restauração de NVS'
STR_INFO_NVS = ''\
' Troca bloco corrompido por dados de backup (não adequado para 10xx/11xx)\n'\
' Aviso - UART e outros sinalizadores podem ser substituídos.\n'\
' Se você precisar definir alguns sinalizadores, faça-o após a recuperação do NVS!\n'\

STR_ABOUT_TORUS_PATCH = 'Sobre a correção de WiFi'
STR_INFO_TORUS_PATCH = ''\
' Será útil em caso de:\n'\
' - FW Torus (WiFi + BT) corrompido\n'\
' - mudar para outro módulo C.I.'\

STR_ABOUT_SB_PATCH = 'Sobre a correção de Chipset(Southbridge)'
STR_INFO_SB_PATCH = ''\
' Será útil em caso de:\n'\
' - FW do Southbridge corrompido ou Erro de "VERSÃO DE EMC DESATIVADA"\n'\
' - Troca por outro módulo C.I. (CXD90046 => CXD90036)\n'\
' - Substituição de Pacotes de APU (21xx => 22xx, 71xx => 72xx)'

STR_INFO_FLASH_TOOLS = ''\
' As ferramentas de gravação (spiway e syscon flasher) são experimentais! Tome cuidado.'\

STR_ABOUT_PART_RECOVERY = 'Análise e recuperação de partição'
STR_INFO_PART_A_R = ''\
' Compara cada byte da partição (SFlash/Syscon) com arquivos válidos\n'\
' e mostra porcentagem de similaridade.\n'\
' A maioria dos arquivos iguais estará no topo da lista.\n'\
' Tenha em mente que FW do Southbridge consiste em EMC + EAP'

STR_INFO_FW_LINK = ''\
' Coloque arquivos emc/eap/torus/syscon válidos na pasta /fws/\n'\
' Você pode baixá-lo deste repositório:\n '

STR_ABOUT_LEG_PATCH = 'Sobre correção Legítima do CoreOS'
STR_INFO_LEG_PATCH = ''\
' Este método é adequado apenas para consoles funcionais!\n'\
' Porque isto requer atualização via menu seguro do PS4\n'\
'\n'\
' 1) Leia o primeiro despejo(dump) (se ainda não o fez)\n'\
' 2) Atualize o console para a MESMA versão via modo de segurança\n'\
' 3) Leia o segundo despejo(dump) (ambos os slots têm FW igual)\n'\
'\n'\
' Agora você pode corrigir o primeiro despejo(dump) com dados do segundo\n'\
' Você pode arrastar e soltar 2 despejos(dumps) no atalho wee-tools para acelerar'

STR_ABOUT_SCF = 'Sobre o gravador de Syscon'
STR_INFO_SCF = ''\
' O gravador de Syscon permite que você grave o chip syscon original do PS4 (RL78/G13)\n'\
' O gravador de Syscon suporta apenas modelos de syscon A0x-COLx\n'\
' Atualmente a parte de hardware é baseada em placas Teensy (2.0++/4.0/4.1)\n'\
' Veja </assets/hw/syscon_flasher> para diagramas e firmware do Teensy\n'\
' Mais informações aqui: '

STR_ABOUT_SPIWAY = 'Sobre o gravador SPIway'
STR_INFO_SPIWAY = ''\
' O gravador SPIway suporta acesso de leitura e gravação em blocos aleatórios (Teensy++ 2.0)\n'\
' Veja a pasta </assets/hw/spiway> para diagramas e firmware do Teensy\n'\
' Mais informações em PSDevWiki: '

STR_ABOUT_SC_GLITCH = 'Sobre o Leitor de Syscon Glitch'
STR_INFO_SC_GLITCH = ''\
' Leitor Syscon da DarkNESmonk (Arduino Nano V3 CH340)\n'\
' Veja a pasta </assets/hw/syscon_reader> para mais informações'

STR_ABOUT_SC_BOOTMODES = 'Sobre Modos de Inicialização'
STR_INFO_SC_BOOTMODES = ''\
' Os registros do modo de inicialização são criptografados, por isso não podemos detectar sua finalidade\n'\
' Você deve experimentar cada um deles sozinho para determinar para que serve\n'\
' Tenha em mente: alguns registros podem ter duplicidades (marcadas com cores)'

STR_OVERCLOCKING = ''\
' Operação perigosa!\n\n'\
' A maioria do GDDR5 funciona entre 6.000-8.000 MHz. GDDR5 tem bombeamento quádruplo [x4]\n'\
' GDDR5 a 8.000 MHz funciona tecnicamente a 2.000 MHz\n'\
' Se você tiver problemas, diminua a frequência para 1.000 MHz\n'\
'\n'\
' A frequência efetiva do GDDR5 é de 1.350 MHz\n'\
' A frequência é selecionada experimentalmente\n'\
' - Valor muito alto pode levar ao erro LOADBIOS -8 ou DCT [*]\n'\
' - Valor muito baixo leva a erro AMDINIT'

STR_ABOUT_EAPKEYS = 'Sobre as chaves EAP'
STR_INFO_EAPKEYS = ''\
' A chave Eap pode ter comprimento de 0x40 e 0x60 bytes\n'\
' Os modelos PS4 10xx/11xx geralmente possuem apenas uma chave\n'\
' E os modelos 12xx/Slim/PRO possuem chave de backup\n'\

STR_IMMEDIATLY = ''\
' Tenha cuidado: todos os patches são aplicados imediatamente ao arquivo!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Alternará o valor entre os valores disponíveis para a opção escolhida'

STR_DOWNGRADE = ''\
' Operação perigosa!\n\n'\
' A comutação de slot é usada para reversão de FW (downgrade).\n'+\
' Ele também corrige o erro “loadbios”.\n'\
' Certifique-se de ter backup completo do firmware de fábrica do SYSCON.\n'\
' É necessário a correção do Syscon! Caso contrário, você receberá o erro "loadbios".\n'\
' O console não inicializa normalmente.'

STR_ABOUT_MPATCH = 'Instruções de correção Manual'
STR_INFO_SC_MPATCH = ''\
' Cada registro tem 16 bytes de comprimento. O primeiro byte é sempre "A5"\n'\
' O segundo byte é o "tipo" de registro, geralmente no intervalo [0x00-0x30]\n'\
' A atualização de firmware leva 4 registros com tipos %s\n'\
' Para cancelar a última atualização do firmware, precisamos limpar esses 4 registros (preencher com 0xFF)\n'\
' Se houver %s,%s tipos após %s a correção será impossível\n'\
' O slot de backup já foi substituído, você receberá um erro checkUpdVersion'

STR_ABOUT_EAP = 'Sobre as chaves EAP'
STR_INFO_HDD_EAP = ''\
' Essas chaves permitem que você explore arquivos no HDD do PS4 com PC\n'\
' Você pode encontrar informações adicionais visitando:\n '\

STR_ABOUT_EMC_CFW = 'Sobre EMC CFW'
STR_INFO_EMC_CFW = ''\
' Use por sua conta e risco!\n'\
' Apenas para Aeolia (PS4 Fat 10xx/11xx)\n'\
' Concede controle sobre o chipset(southbridge) e o syscon\n\n'\
' Informação adicional:\n '

STR_APP_HELP = ''\
' Modo de Usar: ps4-wee-tools [parametros] \n'\
'\n'\
' Parametros: \n\n'\
'  <arquivo>           : carregue a ferramenta apropriada para o arquivo fornecido\n'\
'  <pasta>             : construir despejo(dump) com arquivos da pasta fornecida\n'\
'  <arq1> <arq2> ...   : comparar arquivos (com informações MD5)\n'\
'  --help              : mostrar esta tela de ajuda\n'\
'\n'\
' Homepage: '
