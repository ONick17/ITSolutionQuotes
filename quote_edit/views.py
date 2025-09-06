from django.shortcuts import render, get_object_or_404, redirect
from .forms import QuoteForm
from main.models import Quote



def add_quote(request):
    if request.method == "POST":
        form = QuoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("random_quote")
        else:
            return render(request, "edit_quote.html", {"form": form, "is_new": True, "is_error": True})

    else:
        form = QuoteForm()
    return render(request, "edit_quote.html", {"form": form, "is_new": True, "is_error": False})



def change_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)

    if request.method == "POST":
        form = QuoteForm(request.POST, instance=quote)
        if form.is_valid():
            if form.cleaned_data.get("delete"):
                quote.delete()
            else:
                if form.has_changed():
                    form.save()
            return redirect("random_quote")
        else:
            form = QuoteForm(instance=quote)
            return render(request, "edit_quote.html", {"form": form, "is_new": False, "quote_id": quote.id, "is_error": True})
    
    else:
        form = QuoteForm(instance=quote)

    return render(request, "edit_quote.html", {"form": form, "is_new": False, "quote_id": quote.id, "is_error": False})



def delete_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)

    if request.method == "POST":
        quote.delete()
        return redirect("random_quote")

    return render(request, "delete_quote.html", {"quote": quote})
