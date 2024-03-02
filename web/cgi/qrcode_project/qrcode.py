#!/var/www/cgi-bin/venv/bin/python
import sys,os
import segno
import cgi

def cgi_main():
    print("Content-Type: image/png", end='\n\n')
    # make sure headers are sent first
    sys.stdout.flush()

    form = cgi.FieldStorage()
    msg = form.getfirst("msg", "unknown")
    qrcode = segno.make(msg)
    qrcode.save(sys.stdout.buffer, kind="png", scale=10)

def cmd_main():
    msg = "unknown"
    if len(sys.argv) > 2:
        msg = sys.argv[1]
    qrcode = segno.make(msg)
    qrcode.save(sys.stdout.buffer, kind="png", scale=10)

def main():
    if 'REQUEST_METHOD' in os.environ:
        cgi_main()
    else:
        cmd_main()

if __name__ == '__main__':
    main()

