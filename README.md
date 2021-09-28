# Obsidian Plugins Categorization

[![update-airtable-database](https://github.com/ramisedhom/obsidian-plugins-categorization/actions/workflows/update-airtable-database.yml/badge.svg)](https://github.com/ramisedhom/obsidian-plugins-categorization/actions/workflows/update-airtable-database.yml)
[![export-airtable-to-github-markdown](https://github.com/ramisedhom/obsidian-plugins-categorization/actions/workflows/export-airtable-to-github-markdown.yml/badge.svg)](https://github.com/ramisedhom/obsidian-plugins-categorization/actions/workflows/export-airtable-to-github-markdown.yml)

![GitHub](https://img.shields.io/github/license/ramisedhom/obsidian-plugins-categorization)

Considering that [Obsidian.md](https://obsidian.md) has now 325+ [community or third-party plugins](https://github.com/obsidianmd/obsidian-releases/blob/master/community-plugins.json) which increases on daily bases. With such richness of community contributions, it becomes more difficult to find the proper plugin that help me optimize my notes workflow.

Hence, I did some effort to collect Obsidian.md community plugins and categorize them one-by-one using [Airtable database](https://airtable.com/invite/l?inviteId=invZOB0AEYoqO8gri&inviteToken=d699fe9527edbed243460be2b2e561f9c467867a1145e92e81f64c8d4f4fcafb&utm_source=email).

My main purpose behind this effort is to help myself and others to find the proper plugin for different personal needs after using Obsidian.md.

## Structure

There are two python scripts in this repository:

- UpdateAirtableDatabase.py: Update Airtable database automatically with new and updated plugins,
- ExportAirtableToGithubMarkdown.py: Generate plugins list with associated categories in markdown format.

Those 2 scripts are running daily through [Githab Actions](https://github.com/ramisedhom/obsidian-plugins-categorization/actions) to update plugins list and export new file if needed. 

## Output

- [Airtable database](https://airtable.com/invite/l?inviteId=invZOB0AEYoqO8gri&inviteToken=d699fe9527edbed243460be2b2e561f9c467867a1145e92e81f64c8d4f4fcafb&utm_source=email): you can access this database after creating account on Airtable for free,
- [Categorized Obsidian Community Plugins](./plugins.md)

## Discussions

- [Plugin categorisation on Obsidian Forum](https://forum.obsidian.md/t/plugin-categorisation/13565)
- [Plugin categories on Obsidian Discord](https://discord.com/channels/686053708261228577/888107495233568778)

## Further evolution

Thanks to [Argentina Ortega Sáinz](https://github.com/argenos), this effort had been published on [Obsidian Hub](https://publish.obsidian.md/hub/02+-+Community+plugins/02+-+Community+plugins)

## Contribution

There are several ways to contribute here, either by:

- Review, update and improve categorization on [Airtable database](https://airtable.com/invite/l?inviteId=invZOB0AEYoqO8gri&inviteToken=d699fe9527edbed243460be2b2e561f9c467867a1145e92e81f64c8d4f4fcafb&utm_source=email) or in [Obsidian Hub](https://publish.obsidian.md/hub/02+-+Community+plugins/02+-+Community+plugins),
- Improve the python scripts shared here,
- Suggest new features,
- Create new scripts implementing one of the ideas in "Future Ideas",
- Or may be buy me a coffee to keep be awake at midnight to continue maintaining this project.

## Future Ideas

- Automatically categorize new plugins learning from existing list using some classification ML script,
- Bidirectional synchronization between effort here and community contributions on [Obsidian Community Vault](https://publish.obsidian.md/hub).

## Note

This effort requires me to go continuously through 300+ plugins, as of today, and categorize them. Also to write scripts to update it daily and export them again in readable friendly markdown format.
This is provided to everyone for free, however if you would like to say thanks or help support continued effort, feel free to send a little my way through one of the following methods:

[![ko-fi](https://ko-fi.com/img/githubbutton_sm.svg)](https://ko-fi.com/I2I36CJAV)
