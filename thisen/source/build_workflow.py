from pathlib import Path
from math import atan2, cos, sin, pi
from xml.sax.saxutils import escape
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib import colors
from reportlab.platypus import Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

import argparse

parser = argparse.ArgumentParser(description='Build the nine-page SmartFit360 workflow design PDF.')
parser.add_argument('--output', type=Path, default=Path(__file__).resolve().parent.parent / 'SmartFit360_Complete_Project_Workflow.pdf', help='Destination PDF (default: ../SmartFit360_Complete_Project_Workflow.pdf).')
parser.add_argument('--font-regular', type=Path, help='Optional Arial regular TTF; provide with --font-bold.')
parser.add_argument('--font-bold', type=Path, help='Optional Arial bold TTF; provide with --font-regular.')
args = parser.parse_args()
OUT = args.output.expanduser().resolve()
OUT.parent.mkdir(parents=True, exist_ok=True)
FONT, BOLD = 'Helvetica', 'Helvetica-Bold'
if args.font_regular and args.font_bold and args.font_regular.is_file() and args.font_bold.is_file():
    FONT, BOLD = 'WorkflowArial', 'WorkflowArial-Bold'
    pdfmetrics.registerFont(TTFont(FONT, str(args.font_regular)))
    pdfmetrics.registerFont(TTFont(BOLD, str(args.font_bold)))
    pdfmetrics.registerFontFamily(FONT, normal=FONT, bold=BOLD, italic=FONT, boldItalic=BOLD)
elif args.font_regular or args.font_bold:
    print('Both optional font files must exist; falling back to built-in Helvetica.')
W, H = landscape(A4)
M = 40
NAVY = colors.HexColor('#17354A')
TEAL = colors.HexColor('#087384')
INK = colors.HexColor('#182B3A')
LINE = colors.HexColor('#5F7E8E')
PALE = colors.HexColor('#E9F3F4')
WARM = colors.HexColor('#FFF5D9')
LIGHT = colors.HexColor('#F3F6F8')

styles = {
    'body': ParagraphStyle('Body', fontName=FONT, fontSize=11.3, leading=15, textColor=INK),
    'small': ParagraphStyle('Small', fontName=FONT, fontSize=9.5, leading=12.7, textColor=INK),
    'box': ParagraphStyle('Box', fontName=FONT, fontSize=10.4, leading=13.5, alignment=1, textColor=INK),
    'head': ParagraphStyle('Head', fontName=BOLD, fontSize=21, leading=25, textColor=NAVY),
    'sub': ParagraphStyle('Sub', fontName=BOLD, fontSize=12.2, leading=16, textColor=TEAL),
}
c = canvas.Canvas(str(OUT), pagesize=(W, H), pageCompression=1)
c.setTitle('SmartFit360 Project Workflow and System Architecture')
c.setAuthor('SmartFit360 Team')
c.setSubject('Revised 23 November 2026 to align the supplied coursework reference; proposed design, not validation results')

def para(txt, x, top, width, kind='body', max_h=None):
    p = Paragraph(txt, styles[kind])
    _, height = p.wrap(width, H)
    if max_h is not None and height > max_h:
        raise ValueError(f'Paragraph overflow {height}>{max_h}: {txt[:100]}')
    if top + height > H - 35:
        raise ValueError(f'Page overflow: {top}+{height}: {txt[:90]}')
    p.drawOn(c, x, H-top-height)
    return top+height

def page(title, intro=None):
    para(title, M, 33, W-2*M, 'head')
    if intro:
        para(intro, M, 70, W-2*M, 'body', 46)

def footer(number):
    c.setStrokeColor(colors.HexColor('#CEDBE2'))
    c.setLineWidth(.7)
    c.line(M, 30, W-M, 30)
    c.setFont(FONT, 8)
    c.setFillColor(LINE)
    c.drawString(M, 18, 'SmartFit360 | Workflow and system design | Revision 23 November 2026')
    c.drawRightString(W-M, 18, f'{number} / 9')
    c.showPage()

def box(x, top, width, height, title, detail='', fill=PALE):
    c.setFillColor(fill); c.setStrokeColor(TEAL); c.setLineWidth(.9)
    c.roundRect(x, H-top-height, width, height, 6, fill=1, stroke=1)
    txt = '<b>'+escape(title)+'</b>'
    if detail:
        txt += '<br/>'+escape(detail)
    p = Paragraph(txt, styles['box']); _, ph = p.wrap(width-14, H)
    if ph > height-12:
        raise ValueError(f'Box overflow {title}: {ph}>{height-12}')
    p.drawOn(c, x+7, H-top-(height+ph)/2)
    return (x, top, width, height)

def anchor(b, side):
    x,y,w,h=b
    return {'l':(x,y+h/2), 'r':(x+w,y+h/2), 't':(x+w/2,y), 'b':(x+w/2,y+h)}[side]

def arrow(points):
    c.setStrokeColor(LINE); c.setFillColor(LINE); c.setLineWidth(1.0)
    for a,b in zip(points, points[1:]):
        c.line(a[0], H-a[1], b[0], H-b[1])
    a,b=points[-2:]; ang=atan2(b[1]-a[1], b[0]-a[0]); sz=5
    path=c.beginPath(); path.moveTo(b[0],H-b[1])
    path.lineTo(b[0]-sz*cos(ang-pi/6), H-(b[1]-sz*sin(ang-pi/6)))
    path.lineTo(b[0]-sz*cos(ang+pi/6), H-(b[1]-sz*sin(ang+pi/6)))
    path.close(); c.drawPath(path, fill=1, stroke=0)

def connect(a, sa, b, sb, via=()):
    arrow([anchor(a,sa),*via,anchor(b,sb)])

def table(rows, widths, top, font_size=10.1):
    ps=ParagraphStyle('Cell',fontName=FONT,fontSize=font_size,leading=font_size*1.32,textColor=INK)
    hp=ParagraphStyle('Header',parent=ps,fontName=BOLD,textColor=colors.white)
    data=[[Paragraph(escape(str(v)), hp if i==0 else ps) for v in row] for i,row in enumerate(rows)]
    t=Table(data,colWidths=widths,hAlign='LEFT')
    t.setStyle(TableStyle([
        ('BACKGROUND',(0,0),(-1,0),NAVY),('VALIGN',(0,0),(-1,-1),'MIDDLE'),
        ('GRID',(0,0),(-1,-1),.6,colors.HexColor('#CCD9DF')),
        ('LEFTPADDING',(0,0),(-1,-1),10),('RIGHTPADDING',(0,0),(-1,-1),10),
        ('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),
        ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,LIGHT]),
    ]))
    _,th=t.wrap(W-2*M,H)
    if top+th>H-40: raise ValueError(f'Table overflow at {top} + {th}')
    t.drawOn(c,M,H-top-th)
    return top+th

# Cover: retain the original document purpose and three-module overview.
para('SmartFit360', M, 45, W-2*M, 'head')
para('Project Workflow and System Architecture', M, 83, W-2*M, 'head')
para('Revised design reference | 23 November 2026', M, 124, W-2*M, 'sub')
para('This report connects measurement entry and assisted capture, clothing size advice and one pattern workflow through a reviewed Digital Body Profile. It updates the supplied workflow diagrams to match the current coursework answers. It describes a proposed system; it does not demonstrate a working application or validated measurement station.', M, 165, W-2*M, max_h=75)
table([
    ['Module', 'Purpose and first-release boundary'],
    ['SmartMeasure', 'Manual entry first. Trial phone-camera capture and staged ToF sensor nodes for precisely defined dimensions.'],
    ['SmartFit', 'Explainable rules using approved measurements and a confirmed chart for one supported clothing category.'],
    ['SmartPattern', 'One tailor-reviewed template, required-input checks and an intended full-scale A1 vector PDF.'],
], [130,W-2*M-130], 254, 11)
para('<b>Status convention.</b> Design means a specified proposal. Reported means a statement in the supplied reference that still needs its supporting evidence. Tested means a recorded execution and result; no new test result is claimed in this revision.',M,432,W-2*M,'body',48)
para('<b>Revision basis.</b> SmartFit360_CW1_All_Chapters.docx, especially sections 1.7, 1.9, 2.3, 6.2 and 7.7. The earlier 19 November workflow export is retained in the local source archive. Revision preparation used OpenAI Codex assistance.',M,498,W-2*M,'small',40)
footer(1)

# A: same end-to-end sequence, explicit manual route and reviewed version.
page('A  Overall end-to-end project workflow', 'Research and design lead to a limited connected workflow. SmartFit and SmartPattern use approved profile values, with the exact input version retained.')
b1=box(40,137,160,58,'Research and scope','Client needs and supported category')
b2=box(237,137,160,58,'SmartMeasure','Manual entry or supported capture')
b3=box(434,137,160,58,'Review and correct','Required fields, units and quality')
b4=box(631,137,170,58,'Approve profile','Save a new approved version')
connect(b1,'r',b2,'l');connect(b2,'r',b3,'l');connect(b3,'r',b4,'l')
prof=box(333,240,176,58,'Digital Body Profile','Reviewed values and provenance')
connect(b4,'b',prof,'t',[(716,220),(421,220)])
fit=box(97,345,230,65,'SmartFit','Confirmed chart -> explained size outcome')
pat=box(514,345,230,65,'SmartPattern','Reviewed template -> checked pattern geometry')
connect(prof,'l',fit,'t',[(212,269)]);connect(prof,'r',pat,'t',[(629,269)])
test=box(301,451,240,57,'Validation and release review','Software, measurement and print checks',WARM)
connect(fit,'b',test,'l',[(212,479)]);connect(pat,'b',test,'r',[(629,479)])
para('Manual entry keeps the application usable while assisted capture is evaluated. A missing or rejected measurement returns to retry/manual entry, not to automatic approval. Outputs remain proposals until their separate checks support release.',M,525,W-2*M,'small',26)
footer(2)

# B: replace outdated React/Spring/depth stack throughout.
page('B  System architecture and data flow', 'The proposed application uses Flutter/Dart, FastAPI and PostgreSQL. The laptop runs local capture processing; each ESP32 handles one sensor and USB communication.')
u=box(40,135,155,62,'Customer or tailor','Saved role and permitted records')
app=box(240,135,155,62,'Flutter and Dart','Interface, forms and task context')
api=box(440,135,155,62,'Python FastAPI','Access, validation and approval')
db=box(640,135,161,62,'PostgreSQL','Users, grants, versions and outputs')
connect(u,'r',app,'l');connect(app,'r',api,'l');connect(api,'r',db,'l')
phone=box(40,272,155,62,'Existing phone','Fixed setup through Iriun',WARM)
local=box(240,272,155,62,'Local Python','OpenCV and pretrained MediaPipe',WARM)
draft=box(440,272,155,62,'Candidate draft','Session, source and quality',WARM)
services=box(640,272,161,62,'Backend services','SmartFit rules and pattern rules')
connect(phone,'r',local,'l');connect(local,'r',draft,'l');connect(draft,'t',api,'b');connect(api,'r',services,'t',[(618,166),(618,240),(720,240)])
tof=box(40,411,155,62,'VL53L1X heads','One ordered; up to four after tests',WARM)
esp=box(240,411,155,62,'ESP32 C++ nodes','One controller beside each head')
hub=box(440,411,155,62,'Powered USB data hub','Identified serial requests/replies')
output=box(640,411,161,62,'Version-linked outputs','Fit explanation or A1 pattern PDF')
connect(tof,'r',esp,'l');connect(esp,'r',hub,'l');connect(hub,'t',local,'b',[(517,371),(317,371)]);connect(services,'b',output,'t')
para('The laptop schedules sensor cycles and adds host timing and geometry/session identifiers. Phone frame arrival is not necessarily exposure time. The backend checks access to profiles and files; neither the app nor sensor nodes connect directly to the database.',M,508,W-2*M,'small',38)
footer(3)

# C1: replace automatic girths/depth reconstruction with controlled trials.
page('C1  SmartMeasure measurement workflow', 'Manual measurements are the first route. Assisted capture is an experiment and must not approve unsupported dimensions or replace missing values with zero.')
start=box(40,133,160,58,'Choose task and consent','Retain customer/session context')
manual=box(237,133,160,58,'Manual entry','Agreed definitions and valid units')
review=box(434,133,160,58,'Review and correct','Check required values and source')
approved=box(631,133,170,58,'Approve new version','Continue the original task')
connect(start,'r',manual,'l');connect(manual,'r',review,'l');connect(review,'r',approved,'l')
setup=box(40,259,160,64,'Assisted setup','Phone mount, lighting and geometry',WARM)
camera=box(237,259,160,64,'Camera trial','Landmarks and one defined linear value',WARM)
checks=box(434,259,160,64,'Quality and validity','Reject hidden endpoints or motion',WARM)
retry=box(631,259,170,64,'Retry or manual entry','No automatic release on failure',WARM)
connect(start,'b',setup,'t');connect(setup,'r',camera,'l');connect(camera,'r',checks,'l');connect(checks,'t',review,'b');connect(checks,'r',retry,'l');connect(retry,'t',manual,'b',[(716,224),(317,224)])
node=box(40,396,160,64,'One node then a pair','Confirm carrier and test rigid targets',WARM)
cycle=box(237,396,160,64,'Sequential USB cycle','Complete current identified replies',WARM)
span=box(434,396,160,64,'Paired span','Width/depth at one selected level',WARM)
girth=box(631,396,170,64,'Manual girths','Tape protocol; no automatic girths')
connect(setup,'b',node,'t');connect(node,'r',cycle,'l');connect(cycle,'r',span,'l');connect(span,'t',checks,'b');connect(girth,'t',review,'b',[(716,360),(615,360),(615,212),(514,212)])
para('Opposing heads investigate straight width and front-to-back depth, not circumference. Confirm the delivered carrier before wiring, calibrate each head and the frame, test a pair, then expand to four only if justified. Timeouts, stale or wrongly identified replies invalidate a cycle.',M,490,W-2*M,'small',40)
footer(4)

# C2: keep chart import/fallback while limiting unsupported URL and footwear scope.
page('C2  SmartFit clothing size workflow', 'Start with one supported clothing category and a confirmed size chart. Explainable comparison rules are proposed because trustworthy outcome labels are not yet available.')
labels=[('Open customer task','Load the permitted approved profile'),('Choose product and chart','Supported import or manual entry'),('Validate chart','Source, units, category and meaning'),('Check required values','Request missing data; do not guess')]
nodes=[box(40+i*197,143,160 if i<3 else 170,66,*a) for i,a in enumerate(labels)]
for a,b in zip(nodes,nodes[1:]):connect(a,'r',b,'l')
compare=box(534,285,230,66,'Apply chart comparison rules','Compatible dimensions and relevant ease')
explain=box(77,285,260,66,'Return explained outcome','Suitable size, no suitable size, or insufficient information')
connect(nodes[-1],'b',compare,'t',[(716,247),(649,247)]);connect(compare,'l',explain,'r')
record=box(292,413,260,66,'Save the result provenance','Profile version and chart version used')
connect(explain,'b',record,'l',[(207,446)])
para('If URL import is unsupported, unsafe or unusable, preserve the selected product and offer manual chart entry. First-release scope excludes universal retailer scraping and shoe sizing. A result is advice for the supported chart, not a guarantee of garment fit.',M,510,W-2*M,'small',38)
footer(5)

# C3: retain template input and drafting flow, add exact version/physical scale.
page('C3  SmartPattern template workflow', 'A permitted tailor uses one reviewed template and an approved customer profile. The intended output is an A1 vector PDF at actual size; generation and fit remain to be validated.')
titles=[('Choose permitted customer','Retain customer and template task'),('Load approved profile','Check exact input version'),('Select reviewed template','One supported garment workflow'),('Check required inputs','Block missing values or unsupported rules')]
ns=[box(40+i*197,139,160 if i<3 else 170,68,*v) for i,v in enumerate(titles)]
for a,b in zip(ns,ns[1:]):connect(a,'r',b,'l')
rules=box(563,278,220,65,'Apply reviewed drafting rules','Units, ease and seam allowances')
geometry=box(311,278,220,65,'Construct vector geometry','Reject impossible geometry')
preview=box(59,278,220,65,'Preview and tailor review','Check dimensions and labels')
connect(ns[-1],'b',rules,'t',[(716,242),(673,242)]);connect(rules,'l',geometry,'r');connect(geometry,'l',preview,'r')
pdf=box(185,414,220,65,'Generate A1 PDF at 1:1','Labels, grainline and scale square')
check=box(437,414,220,65,'Separate physical validation','Print scale and tailor assessment',WARM)
connect(preview,'b',pdf,'t',[(169,380),(295,380)]);connect(pdf,'r',check,'l')
para('Store the profile and template versions with each export. A scale check proves print scale only; drafting correctness and garment fit require separate review. Arbitrary image-to-pattern generation and a large template catalogue are outside the first release.',M,510,W-2*M,'small',38)
footer(6)

# C4: version and permission semantics from current coursework reference.
page('C4  Shared profile and validation loop', 'The profile is the shared data layer. Review, permission and immutable input-version links protect both downstream workflows from unapproved or outdated inputs.')
entry=box(40,145,165,70,'Measurement draft','Manual or supported assisted values')
review=box(250,145,165,70,'Permitted review','Correction, units and provenance')
version=box(460,145,165,70,'Approved version V1','Reviewer, source and request ID')
grant=box(670,145,132,70,'Named access','Customer grant and withdrawal')
connect(entry,'r',review,'l');connect(review,'r',version,'l');connect(grant,'l',version,'r')
fit=box(130,304,230,65,'SmartFit result from V1','Keep the chart version and explanation')
pattern=box(482,304,230,65,'SmartPattern export from V1','Keep the template version and file record')
connect(version,'b',fit,'t',[(542,258),(245,258)]);connect(version,'b',pattern,'t',[(542,258),(597,258)])
v2=box(301,437,240,65,'Correction -> review -> V2','Earlier outputs keep V1 and show older-input status',WARM)
connect(fit,'b',v2,'l',[(245,470)]);connect(pattern,'b',v2,'r',[(597,470)])
para('The server checks named access on profile requests, generation and future downloads. A withdrawn grant must prevent future access; it does not alter the recorded input version of an earlier output. Preserve the originating product or template so approval resumes the correct task.',M,525,W-2*M,'small',26)
footer(7)

# D: document history is distinct from invented historical development evidence.
page('D  Revision history and current status', 'This section records the supplied document snapshots and this revision. It does not reconstruct unverified sprint dates, completed experiments or individual contribution history.')
end=table([
    ['Record', 'What it establishes'],
    ['Earlier workflow export - 19 November 2026', 'A planning document existed with the same A-E structure. Its depth-camera and software choices are superseded in this revision.'],
    ['Coursework reference - portfolio dated 21 November 2026', 'Supplied reference for the limited scope, phone/ToF proposal, Flutter/FastAPI stack, resource budget and evaluation plan.'],
    ['This revision - 23 November 2026', 'Aligns the diagrams and written workflow with the current coursework reference. This records a design revision, not a new validation result.'],
], [220,W-2*M-220], 132, 10.3)
para('Current evidence and pending work',M,end+21,W-2*M,'sub')
table([
    ['Area', 'Current position'],
    ['Hardware', 'One sensor order is reported. Delivered carrier, electrical compatibility, capture trial and bench/pair results need checking.'],
    ['Resource plan', 'LKR 91,600 planning ceiling: LKR 81,600 subtotal plus LKR 10,000 contingency. Conditional provisions, not supplier quotations.'],
    ['Application and integration', 'Flutter/Dart, FastAPI and PostgreSQL are the proposed stack. Completed implementation and integrated tests are not established.'],
    ['ML and evaluation', 'Pretrained MediaPipe is proposed. A separate posture classifier is optional and must be compared with rules; no trained custom model or accuracy result is claimed.'],
], [160,W-2*M-160], end+47, 10.2)
footer(8)

# E: preserve practical next steps while removing the obsolete depth-camera dependency.
page('E  Technical notes and next steps', 'Keep acquisition, software tests and physical validation separate. A protocol or diagram is a research/design deliverable; its preparation is not evidence that the test was run.')
para('Implement and test in stages',M,126,W-2*M,'sub')
steps=[
    '<b>1. Confirm scope and references.</b> Agree the first clothing category, chart route, reviewed pattern template, measurement definitions and per-dimension release criteria with the client/tailor.',
    '<b>2. Deliver the manual workflow.</b> Implement accounts, saved roles, named grants, units, review, approval, version links and continuation of the original task before depending on capture.',
    '<b>3. Check the delivered hardware.</b> Confirm sensor and carrier labels, supported power/interface and USB data connections. Trial the fixed phone/Iriun stream, its timing and calibration.',
    '<b>4. Test one head, then an opposing pair.</b> Use known rigid targets, repeated readings and independent straight-span references. Record validity, bias, spread, failures and geometry. Expand to four only if the pair supports the intended use.',
    '<b>5. Evaluate supported capture.</b> Use an agreed consent and reference protocol before human trials. Report errors by dimension, repositioned repeatability, invalid-attempt rate and phone/cycle delay. Manual girths remain separate.',
    '<b>6. Integrate and check outputs.</b> Test access refusal, stale cycles/versions, safe retries, chart fallbacks, missing template inputs and actual-size A1 printing. Retain version, tester, date and result evidence.',
]
y=157
for item in steps:
    y=para(item,M,y,W-2*M,'body',60)+10
para('<b>Progress boundary.</b> No participant recruitment, supplier quote, trained model, passed test or deployed product is implied here. Decide sample size and tolerances in the agreed evaluation protocol; do not reuse an old proposed study count as completed evidence.',M,y+7,W-2*M,'small',40)
footer(9)
c.save()

print(f'Created {OUT}\nPages: 9\nBytes: {OUT.stat().st_size}')
