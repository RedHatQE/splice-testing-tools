class SpliceTestFailed(AssertionError):
    '''
    Splice testing exception
    '''
    pass

def _run_command(connection, command, timeout=60):
    """ Run a command and raise exception in case of timeout or none-zero result """
    status = connection.recv_exit_status(command, timeout)
    if status is not None and status != 0:
        raise SpliceTestFailed("Failed to run %s: got %s return value\nSTDOUT: %s\nSTDERR: %s" % (command, status, connection.last_stdout, connection.last_stderr))
    elif status is None:
        raise SpliceTestFailed("Failed to run %s: got timeout %s\nSTDOUT: %s\nSTDERR: %s" % (command, timeout, connection.last_stdout, connection.last_stderr))

def run_sst(connection, spacewalk_only=False, splice_only=False, timeout=120):
    """ Run spacewalk-splice-tool """
    command = "spacewalk-splice-checkin"
    if spacewalk_only:
        command += " --spacewalk-sync"
    elif splice_only:
        command += " --splice-sync"
    _run_command(connection, command, timeout)

def fake_spacewalk_test(connection, test_name):
    """ Select test with fake spacewalk """
    _run_command(connection, "spacewalk-report-set %s" % test_name)

def fake_spacewalk_step(connection):
    """ Step to next data """
    _run_command(connection, "spacewalk-report-set -n")

def sst_step(connection, fake_spacewalk_connection=None):
    """ Run sst and step to next data (iteration) """
    run_sst(connection)
    if fake_spacewalk_connection is None:
        fake_spacewalk_step(connection)
    else:
        fake_spacewalk_step(fake_spacewalk_connection)

def cleanup_katello(connection, keep_splice=False):
    """ Clean up katello and splice databases """
    _run_command(connection, "katello-configure --reset-data=YES", 300)
    if not keep_splice:
        _run_command(connection, "service splice_all stop ||:")
        _run_command(connection, "mongo checkin_service --eval 'db.dropDatabase()'")
        _run_command(connection, "service splice_all start ||:")
