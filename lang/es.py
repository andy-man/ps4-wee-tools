#==========================================================
# Spanish language [ES]
# part of ps4 wee tools project
# https://github.com/andy-man/ps4-wee-tools
#==========================================================

MENU_SC_REBUILD_MODES = [
	'Modo normal (Elija FW, valores predeterminados para reposo / Todos (12) tipos)',
	'Configuración mínima (Elija los primeros dos tipos y FW/3 tipos)',
	'Modo experto (Ajustar todos los (12) tipos)',
]

MENU_NVS_COPY = [
	'Reemplazar %s con copia de seguridad (%s <= %s)',
	'Reemplazar copia de seguridad con %s (%s => %s)',
]

MENU_EAP_KEYS = [
	'Reemplazar A con B (key_a <= key_b)',
	'Reemplazar B con A (key_a => key_b)',
	'Reparar magia A*',
	'Reparar magia B*',
	'Generar nuevas claves A,B (longitud 0x60) *',
	'Generar nuevas claves A,B (longitud 0x40) *',
	'Limpiar tecla B*',
]

MENU_FLASHER = [
	'Lee todo',
	'Área de lectura',
	'Leer bloque',
	'Escribir todo',
	'Área de escritura',
	'Bloque de escritura',
	'Verificar todo',
	'Verificar área',
	'Verificar bloque',
	'Borrar todo',
	'Borrar área',
	'Borrar bloque',
]

MENU_SERIAL_MONITOR = {
	'Ctrl+Q':'salir del monitor',
	'Ctrl+R':'reiniciar monitor',
	'Ctrl+E':'alternar modo cmd EMC',
	'Ctrl+B':'mostrar códigos de bytes < 0x20',
	'Ctrl+L':'iniciar sesión en el archivo',
}

MENU_TOOL_SELECTION = [
	'Explorador de archivos',
	'Terminal (UART)',
	'sFlash r/w (SPIway de Judges)',
	'Syscon r/w (SCTool de Abkarino & EgyCnq)',
	'Syscon r/o (SCRead de DarkNESmonk)',
	'Syscon w/o (Para stock Renesas RL78)',
	'Cambiar el idioma de la aplicación',
	'Salida',
]

MENU_FILE_SELECTION = {
	'a':'Mostrar todos los archivos/Alternar filtros [bin,pup]',
	'f':'Construir volcado sflash0',
	'b':'Construir 2BLS/PUP',
	'r':'Renombrar lote (extraer información de volcado al nombre de archivo)',
	'c':'Comparar archivos en la carpeta actual',
	'q':'Salir/Regresar',
}

MENU_EXTRA_FLASHER = {
	's':'Seleccionar archivo',
	'f':'Herramienta de inicio para este archivo',
	'q':'Salir/Regresar',
}

MENU_EXTRA = {
	's':'Seleccione otro archivo',
	'f':'Actualizar este archivo (completo/partes) nuevamente a IC',
	'r':'Cambiar el nombre del archivo al nombre canónico',
	'q':'Salir/Regresar',
}

MENU_SFLASH_ACTIONS = [
	'Banderas (UART, RNG, Memtest, etc.)',
	'Reloj de memoria (GDDR5)',
	'Indicador de arranque SAMU',
	'Cambiar ranura CoreOS (revertir FW)',
	'Parche legítimo de CoreOS',
	'Parche Puente Sur',
	'Parche Torus (WiFi+BT)',
	'Herramientas adicionales',
]

MENU_SFLASH_ADV_ACTIONS = [
	'Extraer particiones de sFlash0',
	'Construir sFlash0 a partir de archivos extraídos',
	'Ver / Recuperar áreas NVS (1C9, 1CA)',
	'Ver/Recuperar clave EAP',
	'Obtener claves HDD = descifrar clave EAP = crear [keys.bin]',
	'Crear EMC cfw (sólo para Fat 1xxx/11xx)',
	'Validación de base y estadísticas de entropía',
	'Analizar y recuperar partición corrupta',
]

MENU_SC_ACTIONS = [
	'Alternar depuración',
	'Parche SNVS automático',
	'Visor de bloques SNVS',
	'Visor de bloques NVS',
	'Parche SNVS manual',
	'Herramientas adicionales',
]

MENU_SC_ADV_ACTIONS = [
	'Restablecer contadores SNVS',
	'Selección de modo (00-03)',
	'Modos de arranque (04-07)',
	'Reconstruir SNVS (restablecimiento de fábrica) de Syscon',
	'Recuperar el FW de Syscon',
	'Convertir para intermitente Renesas (Motorolla S28)',
]

MENU_PATCHES = [
	'Método A: se eliminarán los últimos 08-0B (4 registros)',
	'Método B: se limpiarán los últimos 08-0B e inferiores (%d registros)',
	'Método C: limpiar todo lo que esté debajo del 08-0B anterior (%d registros)',
	'Método D: limpiar todo lo que esté debajo del último 08-0B (%d registros)',
	'Método E: limpiar el 08-0B anterior e inferior (%d registros)',
]

MENU_SC_STATUSES = [
	'Ranura CoreOs sobrescrita',
	'Parcheable',
	'Ya parcheado o bloqueado en la actualización',
	'Probablemente parcheable',
]

MENU_SPW_ACTS = {
	'read':		'Lectura',
	'write':	'Escribiendo',
	'verify':	'Verificando',
	'erase':	'Borrar',
}

STR_LANGUAGE			= 'Idioma'
STR_SECONDS				= '%0.0f segundos'
STR_NVS_AREAS			= 'áreas NVS'
STR_PORTS_LIST			= 'Puertos serie'
STR_MAIN_MENU			= 'Menú principal'
STR_FILE_LIST			= 'Lista de archivos'
STR_SFLASH_INFO			= 'sInformación del volcado de Flash'
STR_ADDITIONAL			= 'Herramientas adicionales'
STR_SYSCON_INFO			= 'Información de volcado de Syscon'
STR_COMPARE				= 'Comparar'
STR_HELP				= 'Ayuda'
STR_ACTIONS				= 'Acciones'
STR_COREOS_SWITCH		= 'Cambio de ranura CoreOS'
STR_SWITCH_PATTERNS		= 'Cambiar patrones'
STR_MEMCLOCK			= 'Reloj de memoria'
STR_SAMU_BOOT			= 'Arranque SAMU'
STR_SYSFLAGS			= 'Indicadores del sistema'
STR_NVS_ENTRIES			= 'Syscon %s entradas'
STR_APATCH_SVNS			= 'Parches automáticos de SNVS'
STR_MPATCH_SVNS			= 'Parcheador manual SNVS'
STR_SFLASH_VALIDATOR	= 'Validador sFlash'
STR_SFLASH_FLAGS		= 'Banderas sFlash'
STR_SFLASH_EXTRACT		= 'Extractor de sFlash'
STR_SFLASH_BUILD		= 'Constructor sFlash'
STR_HDD_KEY				= 'Clave eap del disco duro'
STR_2BLS_BUILDER		= 'Constructor 2BLS'
STR_UNPACK_2BLS			= 'Descompactador 2BLS'
STR_UNPACK_PUP			= 'Descompactador de PUP descifrado'
STR_EMC_CFW				= 'EMC CFW (Eolia)'
STR_EAP_KEYS			= 'Claves EAP'
STR_SC_BOOT_MODES		= 'Registros del modo de arranque'
STR_INFO				= 'Información'
STR_SC_READER			= 'Lector Syscon'
STR_SPIWAY				= 'SPIway por Jueces y Abkarino'
STR_SCF					= 'Syscon Flasher de Abkarino y EgyCnq'
STR_LEG_PATCH			= 'Parche legítimo de CoreOS'
STR_PART_RECOVERY		= 'Recuperación de partición'
STR_PART_ANALYZE		= 'Análisis de partición'
STR_PART_LIST			= 'Lista de particiones'
STR_PARTS_INFO			= 'Información de particiones'
STR_WIFI_PATCHER		= 'parcheador WiFi'
STR_SB_PATCHER			= 'Parcheador de Southbridge'
STR_RL78FLASH			= 'RL78 intermitente'
STR_SC_REBUILDER		= 'Reconstructor de Syscon'

STR_ALL					= 'Todos'
STR_UNIQUE				= 'Único'
STR_BACKUP				= 'Copia de seguridad'
STR_EQUAL				= 'Igual'
STR_NOT_EQUAL			= 'No igual'
STR_NO_INFO				= '- Sin información -'
STR_OFF					= 'Desactivado'
STR_ON					= 'Activado'
STR_WARNING				= 'Advertencia'
STR_HELP				= 'Ayuda'
STR_UNKNOWN				= '- Desconocido -'
STR_YES					= 'Sí'
STR_NO					= 'No'
STR_PROBABLY			= 'Probablemente'
STR_NOT_SURE			= 'no estoy seguro'
STR_DIFF				= 'Diferente'
STR_NOT_FOUND			= 'no encontrado'
STR_BAD_SIZE			= 'tamaño incorrecto'
STR_OK					= 'Aceptar'
STR_FAIL				= 'Error'
STR_CANCEL				= 'Cancelar'
STR_IS_PART_VALID		= '[%s] %s FW %s'
STR_SNVS_ENTRIES		= '%d registros encontrados en 0x%05X'
STR_SERIAL_MONITOR		= 'Terminal'
STR_ELAPSEDTIME			= 'Tiempo transcurrido'

STR_NO_PORT_CHOSEN		= ' No se eligió ningún puerto'
STR_NO_PORTS			= ' No se encontró ningún puerto serie'
STR_PORT_UNAVAILABLE	= ' El puerto seleccionado no está disponible'
STR_PORT_CLOSED			= ' El puerto está cerrado'
STR_STOP_MONITORING		= ' El usuario detuvo la supervisión'

STR_RESTART_APP			= ' Reiniciar la aplicación para aplicar los cambios'
STR_GENERATE_ALL_PS		= ' Generar todos los parches'
STR_ACTION_NA			= ' No hay ninguna acción disponible %s'
STR_EMC_CFW_WARN		= ' Actualmente, EMC CFW es solo para PS4 Fat 10xx/11xx'
STR_EMC_NOT_FOUND		= ' No se encontró el FW de EMC'
STR_DECRYPTING			= ' Descifrando'
STR_ENCRYPTING			= ' Cifrando'
STR_PATCHING			= ' Parchear'
STR_EXPERIMENTAL		= ' * - funciones experimentales'
STR_PERFORMED			= ' Acción realizada:'

STR_EMPTY_FILE_LIST		= ' La lista de archivos está vacía'
STR_NO_FOLDER			= ' La carpeta %s no existe'
STR_EXTRACTING			= ' Extrayendo sflash0 a la carpeta %s'
STR_FILES_CHECK			= ' Comprobando archivos'
STR_BUILDING			= ' Creando archivo %s'

STR_DONE				= ' Todo hecho'
STR_PROGRESS			= ' Progreso %02d%%'
STR_PROGRESS_KB			= ' Progreso: %dKB / %dKB'
STR_WAIT				= ' Por favor, espere...'
STR_WAITING				= ' Esperando...'
STR_SET_TO				= ' %s se configuró en [%s]'
STR_ABORT				= ' La acción fue cancelada'
STR_FILENAME			= ' Nombre de archivo: '

STR_VALIDATE_NVS_CHECK	= ' Comprobando áreas NVS'
STR_ACT_SLOT			= ' Ranura activa: %s [0x%02X]'
STR_NIY					= ' La función aún no está implementada'
STR_CLEAN_FLAGS			= ' Limpiar todos los indicadores del sistema'
STR_UNK_FILE_TYPE		= ' Tipo de archivo desconocido'
STR_WRNG_FILE_SIZE		= ' Tamaño de archivo incorrecto'
STR_WRNG_FILE_HEAD		= ' Cabecera de archivo incorrecta'
STR_UNK_CONTENT			= ' Contenido desconocido'
STR_UART				= ' UART está configurado en'
STR_DEBUG				= ' La depuración de Syscon está configurada en '

STR_DIFF_SLOT_VALUES	= ' Los valores en las ranuras son diferentes!'
STR_SYSFLAGS_CLEAN		= ' Se borraron los indicadores del sistema. Consejo: enciende UART'
STR_SAMU_UPD			= ' El indicador SAMU se estableció en'
STR_DOWNGRADE_UPD		= ' El interruptor de ranura se configuró en: '
STR_LAST_SC_ENTRIES		= ' Mostrando las últimas [%d/%d] entradas del bloque activo [%d]'
STR_MEMCLOCK_SET		= ' La frecuencia GDDR5 se configuró en %dMHz [0x%02X]'

STR_RECOMMEND			= ' Método recomendado [%s]'
STR_PATCH_CANCELED		= ' El parche fue cancelado'
STR_PATCH_SUCCESS		= ' %d entradas eliminadas correctamente'
STR_PATCH_SAVED			= ' El parche se guardó en %s'
STR_RENAMED				= ' Renombrado a %s'

STR_SC_BLOCK_SELECT		= ' Seleccionar bloque de datos [0-%d] | Ver Piso/Bloque [f] '
STR_MPATCH_INPUT		= ' Cuántos registros limpiar (desde el final): '
STR_CHOICE				= ' Hacer elección:'
STR_BACK				= ' Presione [ENTER] para regresar'
STR_MEMCLOCK_INPUT		= ' Frecuencia de configuración [400 - 2000] / [0 establecido por defecto (0xFF)] MHz '
STR_SAMU_INPUT			= ' Configurar SAMU [0 - 255] / [el valor predeterminado es 255 (0xFF)] '
STR_TOO_MUCH			= ' %d es demasiado, el valor máximo es %d'
STR_SC_BLOCK_CLEANED	= ' El bloque [%d] se limpió por completo'
STR_OWC_RESET_REQUIRED	= ' Primero debes restablecer los contadores SNVS para realizar esta acción'
STR_SC_NO_BM			= ' No se encontraron registros de modos de arranque!'

STR_UNPATCHABLE			= ' No se puede parchear!'
STR_SYSCON_BLOCK		= ' El bloque [%d/%d] tiene [%d/%d] entradas | El bloque activo es [%d]\n'
STR_PARTITIONS_CHECK	= ' Comprobando particiones'
STR_ENTROPY				= ' Estadísticas de entropía'
STR_MAGICS_CHECK		= ' Comprobando magias'
STR_DUPLICATES			= ' %d duplicados encontrados [%s]'
STR_SC_WARN_OVERWITTEN	= ' Advertencia: CoreOS probablemente esté sobrescrito'

STR_SNVS_ENTRY_INFO		= 'Bloque %d #%03d Desplazamiento 0x%04X'
STR_SC_TOGGLE_FLATDATA	= 'Alternar entre Piso/Bloque'
STR_SH_DUPLICATES		= 'Mostrar/Ocultar duplicados'
STR_NO_ENTRIES			= 'No se encontraron entradas'
STR_SKIPPED				= 'Omitido'
STR_SKIP_ENTRY			= 'Omitir este tipo de entrada'
STR_NO_FILE_SEL			= 'Ningún archivo seleccionado'

STR_INCORRECT_SIZE		= ' %s tiene un tamaño de volcado incorrecto!'
STR_FILE_NOT_EXISTS		= ' El archivo %s no existe!'
STR_FILE_EXISTS			= ' El nombre del archivo ya existe!'
STR_ERROR_FILE_REQ		= ' Primero debes seleccionar el archivo'
STR_SAVED_TO			= ' Guardado en %s'
STR_ERROR_INPUT			= ' Entrada incorrecta'
STR_ERROR_DEF_VAL		= ' Configuración de valores predeterminados'
STR_ERROR_CHOICE		= ' Elección no válida'
STR_ERROR_INFO_READ		= ' Error al leer los datos del archivo'
STR_OUT_OF_RANGE		= ' El valor está fuera de rango!'
STR_FILES_MATCH			= ' Los archivos son iguales'
STR_FILES_MISMATCH		= ' Los archivos no coinciden'
STR_SIZES_MISMATCH		= ' Los tamaños no coinciden!'
STR_RENAMED_COUNT		= ' %d archivos fueron renombrados'
STR_FW_RECORDS			= ' Versiones de FW: desde Actual(1) hasta Inicial(%d)'

STR_SELECT_MODEL		= ' Seleccionar modelo:'
STR_SHOW_DETAILS		= ' Mostrar detalles?'
STR_Y_OR_CANCEL			= ' [y - sí, * - cancelar] '
STR_CHOOSE_AREA			= ' Elegir área:'
STR_INPUT_SEL_DUMP		= ' Seleccionar segundo volcado?'
STR_INPUT_DESTROY_PREV	= ' Destruir todos los registros FW (08-0B) anteriores?'
STR_INPUT_BLOCK			= ' Bloque de inicio de entrada [recuento]: '
STR_INPUT_SAVE_IM		= ' Guardar todos los archivos intermedios?'
STR_INPUT_USE_SLOTB		= ' Usar ranura B (activa)?'
STR_USE_NEWBLOBS		= ' Usar nuevos blobs de claves?'
STR_CONFIRM_SEPARATE	= ' Guardar como archivo independiente?'
STR_CONFIRM				= ' Ingrese [y] para continuar: '
STR_CURRENT				= ' Actual:'
STR_GO_BACK				= ' Regresar'
STR_SC_BM_SELECT		= ' Seleccione la variante del modo de inicio [1-%d] '
STR_OPEN_IN_SC_TOOL		= ' Abrir archivo en Syscon Tool?'
STR_FLASH_FILE			= ' Actualizar este archivo a IC?'

STR_READING_DUMP_N		= ' Volcado de lectura %d'
STR_CHIP_NOT_RESPOND	= ' El chip no responde, verifique el cableado y presione el botón de reinicio'
STR_HOW_MUCH_DUMPS		= ' Cuántos volcados leer? [máximo 10] '

STR_EMC_CMD_MODE		= 'Activando el modo cmd de EMC: [%s]'
STR_SHOW_BYTECODES		= 'Mostrar códigos de bytes < 0x20: [%s]'
STR_MONITOR_STATUS		= 'RX/TX: %d/%d (bytes) transcurrido: %d (seg)'

STR_CHIP_CONFIG			= ' Configuración del chip'
STR_FILE_INFO			= ' Información del archivo'
STR_VERIFY				= ' Verificar'

STR_SPW_PROGRESS		= 'Bloquear %03d [%d KB / %d KB] %d%% %s '
STR_SPW_ERROR_CHIP		= 'Chip no compatible!'
STR_SPW_ERROR_VERSION	= 'Versión no compatible! (v%d.%02d requerido)'
STR_SPW_ERROR_ERASE		= 'Error al borrar el chip!'
STR_SPW_ERROR_ERASE_BLK	= 'Bloque %d - error al borrar el bloque'
STR_SPW_ERROR_DATA_SIZE	= 'Tamaño de datos incorrecto %d'
STR_SPW_ERROR_LENGTH	= 'Longitud incorrecta %d != %d!'
STR_SPW_ERROR_BLK_CHK	= 'Error! Error en la verificación del bloque (bloque=%d)'
STR_SPW_ERROR_WRITE		= 'Error al escribir!'
STR_SPW_ERROR_READ		= 'Tiempo de espera del búfer de recepción diminuto! ¡Desconecta y vuelve a conectar a Teensy!'
STR_SPW_ERROR_VERIFY	= 'Error de verificación!'
STR_SPW_ERROR_PROTECTED	= 'El dispositivo está protegido contra escritura!'
STR_SPW_ERROR_UNKNOWN	= 'Se recibió un error desconocido!'
STR_SPW_ERROR_UNK_STATUS= 'Código de estado desconocido!'
STR_SPW_ERR_BLOCK_ALIGN	= 'Esperando que el tamaño del archivo sea una multiplicación del tamaño del bloque: %d'
STR_SPW_ERR_DATA_SIZE	= 'Los datos tienen %d bytes de longitud (se espera %d)!'
STR_SPW_ERR_OVERFLOW	= 'El chip tiene %d bloques. ¡Escribiendo fuera de la capacidad del chip!'

STR_SCF_ERROR_VERSION	= 'Versión no compatible! (v%d.%02d requerido)'
STR_SCF_ERROR_WRITE_BLK	= 'Error al escribir bloque %d'
STR_SCF_ERROR_ERASE_BLK	= 'Error al borrar el bloque %d'
STR_SCF_ERROR_READ_BLK	= 'Error al leer el bloque %d'
STR_SCF_ERROR_ERASE_CHIP= 'Error durante el borrado del chip'

STR_SCF_ERR_INT			= 'Error durante la inicialización'
STR_SCF_ERR_READ		= 'Error de lectura'
STR_SCF_ERR_ERASE		= 'Borrar error'
STR_SCF_ERR_WRITE		= 'Error de escritura'
STR_SCF_ERR_CMD_LEN		= 'Longitud de comando incorrecta'
STR_SCF_ERR_CMD_EXEC	= 'Error al ejecutar el comando'
STR_SCF_ERR_UNKNOWN		= 'Se recibió un error desconocido!'
STR_SCF_ERR_UNK_STATUS	= 'Código de estado desconocido!'
STR_SCF_SAFE_ERASE		= 'Borrado seguro comenzando en el bloque #%03d'

STR_CANT_USE			= 'No puedo usar esto'
STR_DIFF_SN				= 'Los números de serie son diferentes!'
STR_SSP_EQUAL			= '¡Los patrones de cambio de ranura son iguales!'
STR_LP_FIRST_DUMP		= 'Primer volcado'
STR_LP_SECOND_DUMP		= 'Segundo volcado'

STR_CONVERTING_S28		= ' Conversión al formato S28'
STR_S28_ALREADY			= ' El formato de archivo es S28'

STR_USE_EXPERT_M		= ' Elige otro modelo o usa el modo experto!'
STR_ERR_NO_FW_FOUND		= ' Error: No se puede encontrar %s para el FW %s en la base de datos'
STR_EXPERT_MODE			= ' Modo experto?'
STR_SELECT_FW_VER		= ' Seleccionar versión de firmware'
STR_MODEL				= ' Modelo'
STR_FW_VER				= ' FW: %s / Ranura: %s'
STR_SELECT_MOST_FILE	= ' Seleccionar el archivo más relevante:'
STR_NO_FW_FILES			= ' No se encuentran los archivos! Descargar archivos a la carpeta fws:\n [%s]'

STR_ABOUT_SC_REBUILDER = 'Acerca de Syscon Rebuilder'
STR_INFO_SC_REBUILDER = ''\
' Esta utilidad le ayudará a crear una versión personalizada de Syscon.\n'\
' Puedes ajustar cada tipo de registros en modo experto.\n'\
' Las entradas se ordenan del actual al pasado.\n'\
' * Para seleccionar el FW anterior necesita ingresar "2" o más.\n'\
' * la configuración mínima consta de 3 tipos (00-03 + 04-07 + 08-0B)'

STR_ABOUT_RL78FLASH = 'Acerca de Stock Syscon'
STR_INFO_RL78FLASH = ''\
' Para escribir un nuevo chip syscon en blanco (Renesas RL78G10)\n'\
' necesitas un adaptador USB a TTL, cables y algunos diodos.\n'\
' El diagrama de cableado se puede encontrar en la carpeta activos/hw/l78flash'\

STR_ABOUT_NVS = 'Acerca de la recuperación de NVS'
STR_INFO_NVS = ''\
' Intercambia bloque dañado con datos de respaldo (no apto para 10xx/11xx)\n'\
' Advertencia: Es posible que se sobrescriban UART y otros indicadores.\n'\
' Si necesita configurar algunos indicadores, hágalo después de la recuperación de NVS!\n'\

STR_ABOUT_TORUS_PATCH = 'Acerca del parcheador WiFi'
STR_INFO_TORUS_PATCH = ''\
' Será útil en caso de:\n'\
' - FW Torus (WiFi+BT) dañado\n'\
' - cambiando a otro módulo IC'\

STR_ABOUT_SB_PATCH = 'Acerca del parcheador de Southbridge'
STR_INFO_SB_PATCH = ''\
' Será útil en caso de:\n'\
' - Errores de FW de Southbridge dañados o "EMC VERSION DOWN"\n'\
' - cambiando a otro módulo IC (CXD90046 => CXD90036)\n'\
' - reemplazo de paquetes de APU (21xx => 22xx, 71xx => 72xx)'

STR_INFO_FLASH_TOOLS = ''\
' Las herramientas Flash (spiway y syscon flasher) son experimentales! Ten cuidado.'\

STR_ABOUT_PART_RECOVERY = 'Análisis y recuperación de particiones'
STR_INFO_PART_A_R = ''\
' Compara cada byte de la partición (SFlash/Syscon) con archivos válidos\n'\
' y muestra el porcentaje de similitud.\n'\
' Los archivos más iguales estarán en la parte superior de la lista.\n'\
'Tenga en cuenta que Southbridge FW consta de emc + eap'

STR_INFO_FW_LINK = ''\
' Colocar archivos emc/eap/torus/syscon válidos en la carpeta /fws/\n'\
' Puedes descargarlo desde este repositorio:\n '

STR_ABOUT_LEG_PATCH = 'Acerca del parche legítimo de CoreOS'
STR_INFO_LEG_PATCH = ''\
' ¡Este método sólo es adecuado para consolas que funcionan!\n'\
' Porque requiere actualización a través del menú seguro de PS4\n'\
'\n'\
' 1) Lee el primer volcado (si aún no lo has hecho)\n'\
' 2) Actualice la consola a la MISMA versión a través del modo seguro\n'\
' 3) Leer el segundo volcado (ambas ranuras tienen el mismo FW)\n'\
'\n'\
' Ahora puedes parchear el primer volcado con datos del segundo\n'\
' Puedes arrastrar y soltar 2 volcados en el acceso directo de wee-tools para acelerar'

STR_ABOUT_SCF = 'Acerca de Syscon Flasher'
STR_INFO_SCF = ''\
' Syscon Flasher te permite reproducir/reproducir el chip syscon original de PS4 (RL78/G13)\n'\
' Flasher solo admite modelos de sistema A0x-COLx\n'\
' Actualmente la parte de hardware se basa en placas Teensy (2.0++/4.0/4.1)\n'\
' Mire </assets/hw/syscon_flasher> para ver los diagramas y el firmware de Teensy\n'\
' Más información aquí:'

STR_ABOUT_SPIWAY = 'Acerca de SPIway'
STR_INFO_SPIWAY = ''\
' SPIway - sflash r/w con soporte de acceso de bloque aleatorio (Teensy++ 2.0)\n'\
' Busque en la carpeta </assets/hw/spiway> los diagramas y el firmware de Teensy\n'\
' Más información en PSDevWiki: '

STR_ABOUT_SC_GLITCH = 'Acerca del fallo de Syscon'
STR_INFO_SC_GLITCH = ''\
' Lector Syscon de DarkNESmonk (Arduino Nano V3 CH340)\n'\
' Mire la carpeta </assets/hw/syscon_reader> para obtener más información'

STR_ABOUT_SC_BOOTMODES = 'Acerca de los modos de arranque'
STR_INFO_SC_BOOTMODES = ''\
' Los registros del modo de arranque están cifrados, por lo que no podemos detectar su propósito\n'\
' Deberías probar cada uno de ellos tú mismo para determinar para qué sirve\n'\
' Tenga en cuenta: algunos registros pueden tener duplicados (marcados con color)'

STR_OVERCLOCKING=''\
' ¡Operación peligrosa!\n\n'\
' La mayoría de las GDDR5 funcionan entre 6000 y 8000 MHz. GDDR5 tiene bombeo cuádruple [x4]\n'\
' GDDR5 a 8000 MHz técnicamente funciona a 2000 MHz\n'\
' Si tienes problemas, disminuye la frecuencia a 1000 MHz\n'\
'\n'\
' El reloj GDDR5 efectivo es 1350 MHz\n'\
' La frecuencia se selecciona experimentalmente\n'\
' - Un valor demasiado alto puede provocar un error LOADBIOS -8 o DCT [*]\n'\
' - Un valor demasiado bajo provoca un error AMDINIT'

STR_ABOUT_EAPKEYS = 'Acerca de las claves EAP'
STR_INFO_EAPKEYS = ''\
' La clave Eap puede tener una longitud de 0x40 y 0x60 bytes\n'\
' Los modelos PS4 10xx/11xx normalmente tienen una sola clave\n'\
' Y los modelos 12xx/Slim/PRO tienen clave de respaldo\n'\

STR_IMMEDIATLY = ''\
' Tenga cuidado: ¡todos los parches se aplican inmediatamente al archivo!'

STR_PATCHES = STR_IMMEDIATLY + '\n'\
' Cambiará el valor entre los valores disponibles para la opción elegida'

STR_DOWNGRADE = ''\
' ¡Operación peligrosa!\n\n'\
' El cambio de ranura se utiliza para revertir FW (bajar de categoría).\n'+\
' También corrige el error "loadbios".\n'\
' Asegúrese de tener una copia de seguridad del volcado sFlash y SYSCON.\n'\
' Se requiere parcheo de Syscon! De lo contrario, obtendrás el error "loadbios".\n'\
' La consola no arranca normalmente.'

STR_ABOUT_MPATCH = 'Instrucciones de parche manual'
STR_INFO_SC_MPATCH = ''\
' Cada registro tiene una longitud de 16 bytes. El primer byte siempre es "A5"\n'\
' El segundo byte es el "tipo" de registro, normalmente en el rango [0x00-0x30]\n'\
' La actualización del firmware requiere 4 registros con tipos %s\n'\
' Para cancelar la última actualización de firmware necesitamos limpiar estos 4 registros (rellenar 0xFF)\n'\
' Si hay %s,%s tipos después del parche %s es imposible\n'\
' La ranura de copia de seguridad ya está sobrescrita, obtendrás el error checkUpdVersion'

STR_ABOUT_EAP = 'Acerca de las claves EAP'
STR_INFO_HDD_EAP = ''\
' Estas claves te permiten explorar archivos HDD de PS4 con la PC\n'\
' Puedes encontrar información adicional visitando:\n '\

STR_ABOUT_EMC_CFW = 'Acerca de EMC CFW'
STR_INFO_EMC_CFW = ''\
' Utilízalo bajo tu propia responsabilidad!\n'\
' Sólo para Aeolia (PS4 Fat 10xx/11xx)\n'\
' Otorga control sobre el puente sur y syscon\n\n'\
' Información adicional:\n '

STR_APP_HELP = ''\
' Uso: ps4-wee-tools [parámetros] \n'\
'\n'\
' Parámetros: \n\n'\
' <archivo> : carga la herramienta adecuada para el archivo proporcionado\n'\
' <carpeta> : compila el volcado con archivos de la carpeta proporcionada\n'\
' <archivo1> <archivo2> ... : compara archivos (con información MD5)\n'\
' --help : muestra esta pantalla de ayuda\n'\
'\n'\
' Página de inicio: '
