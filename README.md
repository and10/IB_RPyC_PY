IB_RPyC_PY
==========

Interactive Brokers and CPython bridge using Jython and RPyC

Use:
Install http://rpyc.sourceforge.net/ for CPython and Jython
sudo python setup.py install
sudo jython setup.py install

mkdir rIbServer
mv __init__.py rIbServer/
cp /usr/share/jython/bin/rpyc_classic.py .
jython -Dpython.path=jtsclient.jar rpyc_classic.py

Then from different terminal:
pyton client.py
