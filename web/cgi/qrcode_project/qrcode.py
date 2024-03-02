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

    bg_file = None
    if 'bg' in form:
        if form['bg'].file and form['bg'].filename:
            fname = os.path.basename(form['bg'].filename).lower()
            if fname.endswith(".png") or fname.endswith(".jpg") or fname.endswith(".gif"):
                bg_file = form['bg'].file
    
    writePng(msg, bg_file)

def cmd_main():
    msg = "unknown"
    bg_file = None
    if len(sys.argv) > 1:
        msg = sys.argv[1]
    
    if len(sys.argv) > 2:
        bg_file = open(sys.argv[2], "rb")

    writePng(msg, bg_file)

def writePng(msg, bg_file=None):
    qrcode = segno.make(msg)

    if bg_file is None:
        qrcode.save(sys.stdout.buffer, kind="png", scale=10)
    else:
        qrcode.to_artistic(background=bg_file, target=sys.stdout.buffer, scale=10, kind='png')

def main():
    if 'REQUEST_METHOD' in os.environ:
        cgi_main()
    else:
        cmd_main()

if __name__ == '__main__':
    main()

