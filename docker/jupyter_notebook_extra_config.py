# shutdown the server after no activity for an hour
c.ServerApp.shutdown_no_activity_timeout = 60 * 60
# shutdown kernels after no activity for 30 minutes
c.MappingKernelManager.cull_idle_timeout = 30 * 60
# check for idle kernels every two minutes
c.MappingKernelManager.cull_interval = 2 * 60
# Whether to consider culling kernels which have one or more connections.
c.MappingKernelManager.cull_connected = True
# Whether to consider culling kernels which are busy.
c.MappingKernelManager.cull_busy = False
# Timeout (in seconds) in which a terminal has been inactive and ready to be culled.
c.TerminalManager.cull_inactive_timeout = 30 * 60
c.TerminalManager.cull_interval = 2 * 60

c.Application.log_level = 'WARN'

# Allow deleting non-empty directories from the file browser
c.FileContentsManager.always_delete_dir = True

# Allow users to toggle show/hide hidden files
c.ContentsManager.allow_hidden = True
