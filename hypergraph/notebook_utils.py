"""
simple example script for running and testing notebooks.

Each cell is submitted to the kernel, and the outputs are compared with those stored in the notebook.
"""

import os
import sys
import re

from collections import defaultdict
from queue import Empty

from IPython.kernel import KernelManager
from IPython.nbformat.current import NotebookNode


def sanitize(s):
    """sanitize a string for comparison.

    fix universal newlines, strip trailing newlines, and normalize likely random values (memory addresses and UUIDs)
    """
    if not isinstance(s, str):
        return s
    # normalize newline:
    s = s.replace('\r\n', '\n')

    # ignore trailing newlines (but not space)
    s = s.rstrip('\n')

    # normalize hex addresses:
    s = re.sub(r'0x[a-f0-9]+', '0xFFFFFFFF', s)

    # normalize UUIDs:
    s = re.sub(r'[a-f0-9]{8}(\-[a-f0-9]{4}){3}\-[a-f0-9]{12}', 'U-U-I-D', s)

    return s


def consolidate_outputs(outputs):
    """consolidate outputs into a summary dict (incomplete)"""
    data = defaultdict(list)
    data['stdout'] = ''
    data['stderr'] = ''

    for out in outputs:
        if out.type == 'stream':
            data[out.stream] += out.text
        elif out.type == 'pyerr':
            data['pyerr'] = dict(ename=out.ename, evalue=out.evalue)
        else:
            for key in ('png', 'svg', 'latex', 'html', 'javascript', 'text', 'jpeg',):
                if key in out:
                    data[key].append(out[key])
    return data


def compare_outputs(test, ref, skip_compare=('png', 'traceback', 'latex', 'prompt_number')):
    for key in ref:
        if key not in test:
            print("missing key: %s != %s" % (test.keys(), ref.keys()))
            return False
        elif key not in skip_compare and sanitize(test[key]) != sanitize(ref[key]):
            return False
    return True


def run_cell(shell, iopub, cell):
    shell.execute(cell.input)
    # wait for finish, maximum 20s
    shell.get_msg(timeout=20)
    outs = []

    while True:
        try:
            msg = iopub.get_msg(timeout=0.2)
        except Empty:
            break
        msg_type = msg['msg_type']
        if msg_type in ('status', 'pyin'):
            continue
        elif msg_type == 'clear_output':
            outs = []
            continue

        content = msg['content']
        out = NotebookNode(output_type=msg_type)

        if msg_type == 'stream':
            out.stream = content['name']
            out.text = content['data']
        elif msg_type in ('display_data', 'pyout'):
            out['metadata'] = content['metadata']
            for mime, data in content['data'].items():
                attr = mime.split('/')[-1].lower()
                # this gets most right, but fix svg+html, plain
                attr = attr.replace('+xml', '').replace('plain', 'text')
                setattr(out, attr, data)
            if msg_type == 'pyout':
                out.prompt_number = content['execution_count']
        elif msg_type == 'pyerr':
            out.ename = content['ename']
            out.evalue = content['evalue']
            out.traceback = content['traceback']
        elif msg_type not in ('comm_msg', 'comm_open'):
            print("unhandled iopub msg:", msg_type)

        outs.append(out)
    return outs


def run_notebook(nb):
    km = KernelManager()
    km.start_kernel(extra_arguments=['--pylab=inline'], stderr=open(os.devnull, 'w'))
    kc = km.client()
    kc.start_channels()
    iopub = kc.iopub_channel
    shell = kc.shell_channel

    # run %pylab inline, because some notebooks assume this
    # even though they shouldn't
    shell.execute("pass")
    shell.get_msg()
    while True:
        try:
            iopub.get_msg(timeout=1)
        except Empty:
            break

    successes = 0
    failures = 0
    errors = 0
    for ws in nb.worksheets:
        for cell in ws.cells:
            if cell.cell_type != 'code':
                continue
            try:
                run_cell(shell, iopub, cell)
            except Exception as e:
                print("failed to run cell:", repr(e))
                print(cell.input)
                errors += 1
                continue

            failed = False

            if failed:
                failures += 1
            else:
                successes += 1
            sys.stdout.write('.')

    print("tested notebook %s" % nb.metadata.name)
    print("    %3i cells successfully replicated" % successes)
    if failures:
        print("    %3i cells mismatched output" % failures)
    if errors:
        print("    %3i cells failed to complete" % errors)
    kc.stop_channels()
    km.shutdown_kernel()
    del km
