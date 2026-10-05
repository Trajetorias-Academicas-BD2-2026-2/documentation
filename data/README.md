# Dados do projeto

`raw/` recebe ZIPs oficiais e manifestos com URL, horário, tamanho e SHA-256.
`staging/` recebe CSV normalizado, SQL transacional e relatório de qualidade.
Essas pastas não entram no Git. Não há dados oficiais fabricados neste pacote.

Não reúna arquivos de coortes sobrepostas sem conferir a chave curso + coorte + ano.
Cada revisão deve ter pasta própria. O banco mantém a edição aplicada mais recente
para a chave, e os originais e manifestos preservam a rastreabilidade.
