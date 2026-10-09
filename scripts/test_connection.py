"""Check that Python can talk to a running QLabs instance.

Open QLabs and load a workspace before running this.
"""

from qvl.qlabs import QuanserInteractiveLabs

qlabs = QuanserInteractiveLabs()
connected = qlabs.open("localhost")
print("Connected to QLabs:", connected)
qlabs.close()