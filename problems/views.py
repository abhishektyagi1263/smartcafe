from django.shortcuts import render
from django.http import HttpResponseRedirect,HttpResponse
from django.views.generic import TemplateView
from .models import *
from django.contrib import messages
from django.db.models import Q
import sys
import csv
from django.db.models import Sum
from django.contrib.auth.decorators import login_required
from .decorators import student_required,staff_required
from accounts.models import User
@login_required
@staff_required
def teacher_view(request):
    return render(request,'teacher/teacher.html')
@login_required
@student_required
def test(request):
    items = problem_detail.objects.all()
    context = {
        'items': items,
    }
    if request.method=="POST":
        srch=request.POST['srh']
        if srch:
            match=problem_detail.objects.filter(Q(difficulty__iexact=srch))
            if match:
                return render(request,'problems/test.html',{'sr':match})
            else:
                messages.error(request,'No result found')
        else:
            return HttpResponseRedirect('student/')

    return render(request, 'problems/test.html', context)
@login_required
@student_required
def info(request):
    if request.method=="POST":
        srch=request.POST['asg']
        key=request.POST['xxx']
        key=int(key)
        ass=problem_detail.objects.get(pk=key)
        print(ass.name)
        if srch:
            match=problem_detail.objects.filter(Q(name__iexact=srch))
            if match:
                return render(request,'problems/info.html',{'sr':match,"ass":ass})
            else:
                messages.error(request,'No result found')
        else:
            return HttpResponseRedirect('/info/')


    return render(request,'problems/info.html')

@login_required
@student_required
def subcode(request):
    if request.method == 'POST':


        code_part = request.POST['code_area']
        key=request.POST['hid']
        key=key.strip()
        key=int(key)

        i = problem_detail.objects.get(pk=key)
        user_name=request.POST['user']

        Que_name=i.name
        searching=Response.objects.filter(Q(name=user_name)&Q(question=Que_name)&Q(status="pass"))
        if searching:
            return render(request,'problems/already.html')

        blunder1=""
        blunder2=""


        def input():
            a = i.input1

            return a
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = str(e).strip()
            blunder1+=str(e).strip()
        print('first output',output,type(output))
        x=[]
        x.append(output)

        def input():
            a = (i.input2)

            return a
        try:
            orig_stdout = sys.stdout
            sys.stdout = open('file.txt', 'w')
            exec(code_part)
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = open('file.txt', 'r').read()
        except Exception as e:
            sys.stdout.close()
            sys.stdout=orig_stdout
            output = str(e).strip()
            blunder2+=str(e).strip()
        print('second output',output,type(output))
        x.append(output)
        b=[]
        for e in x:
            b.append(e.strip())
        print('is is strip of user')
        print(b)
        b2=[]
        y1=i.output1.replace('\r',' ')
        y2=i.output2.replace('\r',' ')
        b2.append(y1)
        b2.append(y2)
        print(b2)


        r=Response()
        flag=0

        if b[0]==blunder1:
            x=blunder1
            flag=1
            res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
            return res
        elif  b[1]==blunder2:
            x=blunder2
            flag=1
            res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
            return res
        elif b[0]==b2[0] and b[1]==b2[1]:
            x="Congrats All Testcases Pass"
            r.status="pass"
            r.marks=2

        else:
            x="Try Again"
            r.status="fail"
            r.marks=0

        r.submittion="Submitted"
        r.user_user=request.POST['user']
        r.user_id=request.POST['id']
        r.ass_ass=i.name
        r.ass_id=i.no
        r.name=request.POST['user']
        r.code=request.POST['code_area']
        r.question=i.name


        r.save()

    res = render(request,'problems/sub.html',{"code":code_part,"output":x,"flag":flag})
    return res
@login_required
@student_required
def result(request):
    user=request.user
    print(user.id)
    verma=Response.objects.filter(Q(name__icontains=user))
    print(verma)
    return render(request,'problems/result.html',{'user':user,'verma':verma})
@login_required
@staff_required
def ques(request):
    prob1=problem_detail.objects.all()
    if request.method=='POST':
        prob=problem_detail()
        prob.no=request.POST['no']
        prob.name=request.POST['name']
        prob.difficulty=request.POST['difficulty']
        prob.info=request.POST['info']
        prob.que=request.POST['question']
        prob.input1=request.POST['input1']
        prob.input2=request.POST['input2']
        prob.output1=request.POST['output1']
        prob.output2=request.POST['output2']
        prob.save()
        return render(request,'teacher/statements.html',{'prob':prob1})
    else:
        return render(request,'teacher/ques.html')
@login_required
@staff_required
def submittion(request):
    sub=Response.objects.all()
    if request.method=='POST':
        name=request.POST['abhi']
        exp=Response.objects.filter(Q(name__icontains=name) | Q(question__icontains=name) | Q(status__icontains=name) )

        return render(request,'teacher/submittion.html',{'sub':exp})

    return render(request,'teacher/submittion.html',{'sub':sub})
@login_required
@staff_required
def stat(request):
    prob=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':prob})
@login_required
@staff_required
def deleteQue(request,id):
    print(id)

    x=problem_detail.objects.filter(name=id)
    x.delete()
    prob=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':prob})
@login_required
@staff_required
def edit_que(request,id):
    x=problem_detail.objects.get(name=id)
    fields={'no':x.no,'name':x.name,'difficulty':x.difficulty,'info':x.info,'que':x.que,'input1':x.input1,'input2':x.input2,'output1':x.output1,'output2':x.output2}
    return render(request,'teacher/edit.html',fields)
@login_required
@staff_required
def final(request):
    fin=request.POST['imp']
    x=problem_detail.objects.get(no=fin)
    x.no=request.POST['no']
    x.name=request.POST['name']
    x.difficulty=request.POST['difficulty']
    x.info=request.POST['info']
    x.que=request.POST['question']
    x.input1=request.POST['input1']
    x.input2=request.POST['input2']
    x.output1=request.POST['output1']
    x.output2=request.POST['output2']
    x.save()
    x=problem_detail.objects.all()
    return render(request,'teacher/statements.html',{'prob':x})
@login_required
@student_required
def code(request,id):
    print(id)
    x=Response.objects.get(id=id)
    return render(request,'problems/view_code.html',{'x':x})
@login_required
@staff_required
def export(request):
    response=HttpResponse(content_type='text/csv')
    writer=csv.writer(response)
    writer.writerow(['No','Name','Problem Name','Submission','Status','Marks','Code'])
    for members in Response.objects.all().values_list('id','name','question','submittion','status','marks','code'):
        writer.writerow(members)
    response['Content-Disposition']='attachment;filename="members.csv"'
    return response
@login_required
@staff_required
def teacher_view_code_fun(request,id):
    print(id)
    x=Response.objects.get(id=id)
    return render(request,'teacher/teacher_view_code.html',{'x':x})
@login_required
@staff_required
def analysis(request):

        total_pb=problem_detail.objects.count()
        usernames = User.objects.filter(is_student=True).values_list('username', flat=True)

        p=[]
        f=[]
        marks_list=[]
        pp_list=[]
        assignment_list=[]
        for i in usernames:
            passed=Response.objects.filter(Q(name__icontains=i)).filter(status='pass').count()
            failed=Response.objects.filter(Q(name__icontains=i)).filter(status='fail').count()
            total=Response.objects.filter(Q(name__icontains=i)).count()
            if total==0:
                attempts_percent=str("0%")
                percent_asg=str("0%")
            else:
                attempts_percent=str(int((passed*100)/total))+"%"
                percent_asg=str(int((passed*100)/total_pb))+"%"
            marks=2*passed
            p.append(passed)
            f.append(failed)
            pp_list.append(attempts_percent)
            assignment_list.append(percent_asg)
            marks_list.append(marks)
        # print(usernames)
        # print(p)
        # print(f)
        # print(pp_list)
        # print(assignment_list)
        # print(marks_list)
        #
        # if request.method=='POST':
        #     name=request.POST['ab']
        #     s=Response.objects.filter(Q(name__icontains=name)).filter(status='pass').count()
        #     f=Response.objects.filter(Q(name__icontains=name)).filter(status='fail').count()
        #     total=Response.objects.filter(Q(name__icontains=name)).count()
        #     total_pb=problem_detail.objects.count()
        #     if total==0:
        #         attempts_percent=str("0%")
        #         percent_asg=str("0%")
        #     else:
        #         attempts_percent=str(int((s*100)/total))+"%"
        #         percent_asg=str(int((s*100)/total_pb))+"%"
        #     marks=2*s

        return render(request,'teacher/analysis.html',{'p':p,'f':f,'marks_list':marks_list,'assignment_list':assignment_list,'pp_list':pp_list,'name':usernames})
@login_required
@staff_required
def ex(request):
    response=HttpResponse(content_type='text/csv')
    writer=csv.writer(response)
    writer.writerow(['Name','Passed Files','Failed Files','Marks','Pass Percent','Assignment Completed'])
    total_pbe=problem_detail.objects.count()
    usernamese = User.objects.filter(is_student=True).values_list('username', flat=True)
    for i in usernamese:
        passede=Response.objects.filter(Q(name__icontains=i)).filter(status='pass').count()
        failede=Response.objects.filter(Q(name__icontains=i)).filter(status='fail').count()
        totale=Response.objects.filter(Q(name__icontains=i)).count()
        if totale==0:
            attempts_percente=str("0%")
            percent_asge=str("0%")
        else:
            attempts_percente=str(int((passede*100)/totale))+"%"
            percent_asge=str(int((passede*100)/total_pbe))+"%"
        markse=2*passede
        writer.writerow([i,passede,failede,markse,attempts_percente,percent_asge])
    response['Content-Disposition']='attachment;filename="analysis.csv"'
    return response
