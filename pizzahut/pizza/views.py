from django.shortcuts import render
from .forms import PizzaForm  #here . refers to importing current file from same file
from .forms import MultiplePizzaForm
from django.forms import formset_factory
from .forms import Pizza

# Create your views here.
def homepage(request):
    return render(request,'home.html')

def orderpage(request):
    multiple_form = MultiplePizzaForm()
    if request.method == 'POST':
        created_pizza_pk = None  #for editing
        filled_form = PizzaForm(request.POST)  #collect filled form
        if filled_form.is_valid():   #validate the form
            note = 'Thanks,your order %s,%s and %s pizza placed!!'%(filled_form.cleaned_data['topping1'],
                                                                    filled_form.cleaned_data['topping2'],
                                                                    filled_form.cleaned_data['size'])
            created_pizza=filled_form.save()
            created_pizza_pk = created_pizza.id
            #print(filled_form['topping1'])
            #print(filled_form.cleaned_data['topping1'])
        else:
            note = 'Sorry Try Again..'
        new_form = PizzaForm()
        return render(request, 'order.html',{'pizzaform': new_form,'multiplepizzaform':multiple_form,'note':note,'created_pizza_pk':created_pizza_pk}) #returning new form and note
    else:
        form = PizzaForm()
        return render(request, 'order.html',{'pizzaform':form,'multiplepizzaform':multiple_form})

def pizzas(request):
    no_of_pizzas = 2
    if request.method == 'GET':
        filled_form = MultiplePizzaForm(request.GET)  #collect filled form
        if filled_form.is_valid():
            no_of_pizzas=filled_form.cleaned_data['number']
            print(no_of_pizzas)
    pizza_form_set = formset_factory(PizzaForm,extra=no_of_pizzas)  #formset class
    formset = pizza_form_set()  #empty formset

    if request.method =='POST':
        filled_formset = pizza_form_set(request.POST)
        if filled_formset.is_valid():
            for form in filled_formset:
                form.save()
            note = 'Congrats Order Placed!!'
        else:
            note = 'Sorry Tryagain...'
        return render(request, 'pizzas.html', {'note':note})
    else:
        return render(request,'pizzas.html',{'formset':formset})

def edit(request,pk):  # for identify the passed pk or model obj /instance
    pizza_obj = Pizza.objects.get(pk=pk)  #form obj/instance
    form = PizzaForm(instance=pizza_obj)
    if request.method == 'POST':
        filled_form = PizzaForm(request.POST,instance=pizza_obj)
        if filled_form.is_valid():
            filled_form.save()
            note = 'Order Edited Successfully!!'
        else:
            note = 'Please Try Again...'
        return render(request,'edit.html',{'note':note,'pk':pk})
    else:
        return render(request,'edit.html',{'form':form,'pk':pk})



#after saving the form the created pk shows the edit order option and passing the pk to the edit page-it should come in order.html after h2 tag