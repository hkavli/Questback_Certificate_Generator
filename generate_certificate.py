import sys
import os
import os.path
from datetime import datetime
from reportlab.pdfgen import canvas
from reportlab.lib import utils
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.pagesizes import A4
from reportlab.platypus import Frame, Image

# Globale constants - > endres til kursholder og boss
WIL = "Wilhelm Hødnebø"
HAK = "Håkon Kavli"
QB = "Questback AS"
NAM = "Nordic Academy Manager"
HSA = "Head of Support and Training"
TITLE = "Questback Essentials Certified User"

# Norwegian text elements
norIssuedTo = "tildeles"
norIssuedBecause = "For gjennomføring av:"
norFrom = "fra"
blank = " "
THE = "den"
IN = "i"

# Swedish text elements
sweIssuedTo = "tilldelas"
sweIssuedBecause = "För deltagande på"
sweFrom = "från"


# Variables
date = datetime.now()
today = date.strftime("%d.%m.%Y")


# Base colors
hexBaseBlaa = "#315665"
hexBaseGraa = "#919191"
hexBaseGroenn = "#74b5a5"

# Accent colors
hexGraa = "#e8e6df"
hexBlaa = "#709bb6"
hexRoed = "#fd8770"
hexGul = "#feca79"
hexGroenn = "#2bcb75"
hexSvart = "#000000"
hexHvit = "#ffffff"

# Scale the logo for maintaining its proportions


def get_image(path, width):
    img = utils.ImageReader(path)
    iw, ih = img.getSize()
    aspect = ih / float(iw)
    return Image(path, width=width, height=(width * aspect))


# Draws the certicicate elements


def generate_certificate(attestID, navn, firmanavn, kursnavn, kursdato, kurssted, kursnavn2, kursdato2, pdf_filename, navnASCII):
    attestID += 1
    with open(pdf_filename, "w+") as f:
        # Geometry
        c = canvas.Canvas(pdf_filename, pagesize=A4)
        width = A4[0]
        height = A4[1]
        x = 0
        halfWidth = width/2
        quarterWidth = width/4
        threeQuarterWidth = quarterWidth*3

        # Draws basic properties, incl. filling the canvas with the desired color and adding a background logo
        frame = Frame(0, 0, width, height-2*cm, showBoundary=False)
        c.setFillColor(HexColor(hexBaseGroenn))
        b = c.beginPath()
        b.moveTo(x, x)
        b.lineTo(x, height)
        b.lineTo(width, height)
        b.lineTo(width, x)
        c.drawPath(b, True, True)
        c.drawImage('img/questback_mark.png', 5, (height/4),
                    width=(1776/3), height=(1182/3), mask='auto')
        c.setStrokeColor(HexColor(hexHvit))
        c.setFillColor(HexColor(hexHvit))
        c.setFont('Helvetica-Bold', 52, leading=True)
        c.drawCentredString((halfWidth), 675, 'academy')

        # Draws language specific properties
        try:
            if kurssted == "Oslo" or kurssted == "Trondheim":
                c.setFont('Helvetica-Bold', 32, leading=True)
                c.drawCentredString(halfWidth, 550, TITLE)
                c.setFont('Helvetica-Bold', 34, leading=False)
                c.drawCentredString(halfWidth, 450, navn)
                c.setFont('Helvetica', 24, leading=False)
                c.drawCentredString(halfWidth, 500, norIssuedBecause)
                c.drawCentredString(
                    halfWidth, 400, norFrom + blank + firmanavn)
                c.drawCentredString(halfWidth, 350, norIssuedTo)
                c.drawCentredString(halfWidth, 300, kursnavn +
                                    blank + THE + blank + kursdato)
                c.drawCentredString(halfWidth, 275, kursnavn2 +
                                    THE + blank + kursdato2)
                c.drawCentredString(halfWidth, 250, IN + blank + kurssted)
                c.setFont('Helvetica', 18, leading=False)
                c.drawCentredString(quarterWidth, 100, WIL)
                c.drawCentredString(quarterWidth, 75, HSA)
                c.drawCentredString(quarterWidth, 50, today)
                c.drawCentredString(threeQuarterWidth, 100, HAK)
                c.drawCentredString(threeQuarterWidth, 75, NAM)
                c.drawCentredString(threeQuarterWidth, 50, today)
            elif kurssted == "Stockholm":
                c.setFont('Helvetica-Bold', 32, leading=True)
                c.drawCentredString(halfWidth, 550, TITLE)
                c.setFont('Helvetica-Bold', 34, leading=False)
                c.drawCentredString(halfWidth, 450, navn)
                c.setFont('Helvetica', 24, leading=False)
                c.drawCentredString(halfWidth, 500, sweIssuedTo)
                c.drawCentredString(
                    halfWidth, 400, sweFrom + blank + firmanavn)
                c.drawCentredString(halfWidth, 350, sweIssuedBecause + blank)
                c.drawCentredString(halfWidth, 300, kursnavn +
                                    blank + THE + blank + kursdato)
                c.drawCentredString(halfWidth, 275, kursnavn2 +
                                    blank + THE + blank + kursdato2)
                c.drawCentredString(halfWidth, 250, IN + blank + kurssted)
                c.setFont('Helvetica', 18, leading=False)
                c.drawCentredString(quarterWidth, 100, WIL)
                c.drawCentredString(quarterWidth, 75, HSA)
                c.drawCentredString(quarterWidth, 50, today)
                c.drawCentredString(threeQuarterWidth, 100, HAK)
                c.drawCentredString(threeQuarterWidth, 75, NAM)
                c.drawCentredString(threeQuarterWidth, 50, today)
        except Exception as err:
            print("Tegningen feilet %s\n%s" % (pdf_filename, err))

        # Draws a line below signatures
        c.setLineJoin(mode=2)
        c.setLineWidth(1)
        p = c.beginPath()
        p.moveTo(50, 122)
        p.lineTo(250, 122)
        p.close()
        p.moveTo(350, 122)
        p.lineTo(550, 122)
        p.close()
        c.drawPath(p, fill=1, stroke=1)

        # Adds signatures (use e.g. https://onlinepngtools.com/create-transparent-png to flaten new signatures (remove any noise)
        c.drawImage('img/wilhelm.png', 50, 110, width=200,
                    height=100, mask=[0, 0, 0, 0, 0, 0])
        c.drawImage('img/hakon.png', 350, 110, width=200,
                    height=100, mask=[0, 0, 0, 0, 0, 0])

        story = []
        story.append(get_image('img/questback_white.png', width=width/1.25))
        frame.addFromList(story, c)
        c.showPage()
        c.save()
        f.close()

        print(f"Sertifisering for {navnASCII} er generert")
        return attestID
