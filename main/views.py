import random
from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import F, Q
from main.models import Quote



def random_quote(request):
    quotes = Quote.objects.values("id", "weight")
    if not quotes.exists():
        return render(request, "random_quote.html", {"quote": None})

    total_weight = sum(q["weight"] for q in quotes)
    random_weight = random.randint(1, total_weight)
    current_weight = 0

    quote_id = None
    for q in quotes:
        current_weight += q["weight"]
        if current_weight >= random_weight:
            quote_id = q["id"]
            break

    Quote.objects.filter(pk=quote_id).update(views = F("views")+1)
    quote = Quote.objects.get(pk=quote_id)
    return render(request, "random_quote.html", {"quote": quote})



def like_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)
    Quote.objects.filter(pk=id).update(likes = F("likes")+1)
    return redirect("random_quote")



def dislike_quote(request, id):
    quote = get_object_or_404(Quote, pk=id)
    Quote.objects.filter(pk=id).update(dislikes = F("dislikes")+1)
    return redirect("random_quote")



def top_quotes(request):
    # top10 = Quote.objects.order_by("-likes")[:10]
    # return render(request, "top_quotes.html", {"quotes": top10})
    text_query = request.GET.get("text", "")
    source_query = request.GET.get("source", "")

    quotes = Quote.objects.all()

    if text_query:
        quotes = quotes.filter(text__icontains=text_query)

    if source_query:
        quotes = quotes.filter(source__icontains=source_query)

    quotes = quotes.order_by("-likes")[:10]

    return render(
        request,
        "top_quotes.html",
        {"quotes": quotes, "text_query": text_query, "source_query": source_query},
    )



def page_404(request, exception=None):
    return render(request, "my_404.html", status=404)
