# Changelog

Todas mudanças pertinentes a biblioteca serão documentadas aqui. O formato utilizado se baseia no [_Keep a Changelog_](https://keepachangelog.com/en/1.1.0/) e esse projeto adota o [_Semantic Versioning_](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

> Sem modificações.

## [v0.0.1](https://github.com/aiboxlab/data-lake/releases/tag/v0.0.0) - 2025-09-12

### Added

- Versão inicial da biblioteca;
- Adição das interfaces básicas e CLI;

## [v0.0.2](https://github.com/aiboxlab/data-lake/releases/tag/v0.0.2) - 2025-09-11

### Added

- Melhorias no CLI;
- Adição de CHANGELOG;

## [v0.0.3](https://github.com/aiboxlab/data-lake/releases/tag/v0.0.3) - 2025-09-14

### Added

- Novo método para listagem de fontes de dados disponíveis no sistema;
    - Novo comando no CLI adicionado;

### Fixed

- Correção no carregamento de fontes dados: adição de sufixo `/` no `dataPath`;
    - Nova modificação agora garante que apenas uma fonte de dados é selecionada;
    - Anteriormente, caso existissem diferentes fontes de dados com mesmo prefixo ambas seriam selecionadas nos blobs;
