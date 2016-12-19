## TheVoxFox Usage: !msync

TheVoxFox accepts a small range of arguments that you can use to retrieve modulesync version states or generate reports.

Learn more about modulesync [here](https://github.com/voxpupuli/modulesync_config)

Using `!msync` with no args will retrieve the latest semver tag from our modulesync_config repo.

### Args

#### getver

Query the last modulesync config version applied to a specific repo.

Example: `!msync getver puppet-network`

#### olderthan and newerthan

Generate a report of all modules older/newer than and equal to a given semver.

Example: `!msync olderthan 0.16.0`

#### current

Generate a report of all modules whose msync versions are up to date.
