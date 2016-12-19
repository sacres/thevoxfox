## TheVoxFox Usage: !msync

TheVoxFox accept a small range of arguments that you can use to retrieve modulesync version statues or generate reports.

Using `!msync` with no args will retrieve the latest semver tag from our modulesync_config repo.

### Args

#### getver

Query the last applied modudlesync config version applied to a specific repo. 

Example: `!msync getver puppet-network`

#### olderthan and newerthan

Generate a report of all modules older/newer than and equal to a given semver.

Example: `!msync olderthan 0.16.0`

#### current

Generate a report of all modules whose msync versions are up to date.
