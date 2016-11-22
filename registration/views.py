from django.shortcuts import render
from django.http import Http404
from .models import Visitor
from django.views.generic.edit import CreateView
from django import forms
import xlwt

# renders the home page of the app


def index(request):
    return render(request, 'registration/index.html')


# passing primary key of the visitor object to get details of the visitor

def detail(request, pk):
    try:
        visitor = Visitor.objects.filter(id=pk)
    except Visitor.DoesNotExist:
        raise Http404("There is no visitor with the id = ", pk)

    else:
        context = {
            'all_visitors': visitor
        }

    return render(request, 'registration/all.html', context)

# show details of a single user
def showdetail(request):
    try:
        visitor = Visitor.objects.get(id=request.POST['Visitor'])
    except Visitor.DoesNotExist:
        raise Http404("There is no visitor with the id = ", visitor.id)

    context = {
        'all_visitors': visitor,
        'successMsg': 'Thank you for visiting. Please proceed for access'
    }

    return render(request, 'registration/all.html', context)


# show details of all users
def showallvisitors(request):
    all_visitors = Visitor.objects.all()
    context = {
        'all_visitors': all_visitors
    }
    return render(request, 'registration/all.html', context)


# show details of all users
def showallvisitorswithfilter(request):
    all_visitors = Visitor.objects.all()
    context = {
        'all_visitors': all_visitors
    }
    return render(request, 'registration/filtered.html', context)


# render the register form to create a visitor object
class RegisterView(CreateView):
    model = Visitor
    # renders labels and fields to visitor_form template automatically
    fields = ['firstName', 'lastName', 'email', 'phone', 'visitingPerson']


# filter the visitors based on from and to dates selected
def filtervisitors(request):
    try:
        if not str(request.GET['fromDate']) or not str(request.GET['toDate']):
            raise forms.ValidationError("Both From Date and To Date should be given")
        else:
            filteredvisitors = Visitor.objects.filter(created_at__range=[str(request.GET['fromDate']), str(request.GET['toDate'])])
            context = {
                'all_visitors': filteredvisitors
            }
    except forms.ValidationError:
        return render(request, 'registration/filtered.html', {'all_visitors': [],
                                                         'errorMsg': "Both From Date and To Date should be given"})

    return render(request, 'registration/filtered.html', context)


# parses the string querySet objects obtained from template and saves to a excel workbook
# It took a lot of time to write this function, slighlty complicated given that querySet is not a readable object

def exporttoexcel(request):
    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet("Sheet 1")
    # Define the header fonts and style
    header_font = xlwt.Font()
    header_font.bold = True
    table_header = xlwt.XFStyle()
    table_header.font = header_font

    column_titles = ['Id', 'First Name', 'Last Name', 'Phone', 'Email', 'Visiting']
    # write header in bold
    for col, item in enumerate(column_titles):
        sheet.write(0, col, item, table_header)

    # list comprehension to remove unicode u' from querySet
    filtered_visitors_unicode = [value for name, value in request.POST.iteritems() if name.startswith('filtered_visitors')]
    filtered = [x.encode('UTF8') for x in filtered_visitors_unicode]
    filteredObjs = filtered[0].split('>')

    # populate filteredList by just getting the necessary info provided by Visitor.__str__() output
    filteredList = []
    for item in filteredObjs:
        if item.find(": ") != -1:
            visitorstr = item.split(": ", 1)[1]
            filteredList.append(visitorstr.split(","))

    # write to workbook
    for i, v in enumerate(filteredList):
        for x in range(0, 6):
            sheet.write(i+1, x, v[x])

    # saves the excel to visitorsLog project's root directory
    workbook.save('VisitorsData.xls')

    list_of_ids = [x[0] for x in filteredList]

    return render(request, 'registration/filtered.html', {'all_visitors': Visitor.objects.filter(pk__in=list_of_ids)})
