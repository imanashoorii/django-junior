import json

from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404

from watchlist.models import WatchItem


def list_create_view(request):
    if request.method == "GET":
        items = WatchItem.objects.all().order_by("-created_at")
        return render(request, "list_create.html", {"items": items})
    if request.method == "POST":
        title = request.POST.get("title")
        type = request.POST.get("type")
        poster = request.FILES.get("poster")
        url = request.POST.get("url")

        WatchItem.objects.create(
            title=title,
            type=type,
            poster=poster,
            url=url,
        )
        items = WatchItem.objects.all().order_by("-created_at")
        return render(
            request,
            "list_create.html",
            {"message": "new item added successfully", "items": items},
        )
    return JsonResponse({"message": "Invalid Request"}, status=405)


def detail_view(request, pk):
    item = get_object_or_404(WatchItem, pk=pk)
    return render(request, 'detail_item.html', {'item': item })

def update_view(request, pk):
    item = get_object_or_404(WatchItem, pk=pk)
    return render(request, 'update_item.html', {'item': item })

def update_api_view(request, pk: int) -> JsonResponse:
    if request.method not in ["PUT", "PATCH"]:
        return JsonResponse({"error": "Method Not Allowed"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except json.JSONDecodeError:
        return JsonResponse(
            {"message": "Invalid JSON format!", "is_ok": False},
            status=400
        )

    if request.method == "PUT":
        title = data.get("title", None)
        item_type = data.get("type", None)

        if not title or not item_type:
            return JsonResponse(
                {
                    'message': "It is not possible to save an item without entering a 'title' and 'type'.",
                    'is_ok': False
                },
                status=400
            )

        item = get_object_or_404(WatchItem, pk=pk)
        item.title = title
        item.type = item_type
        item.url = data.get("url")
        item.is_watched = data.get("is_watched", False)
        item.save()

        return JsonResponse(
            {
                'message': "selected item successfully updated",
                'is_ok': True
            },
            status=200
        )

    if request.method == "PATCH":
        is_watched = data.get("is_watched", None)
        if (
                "is_watched" not in data
                or not isinstance(data["is_watched"], bool)
        ):
            return JsonResponse(
                {
                    'message': "Invalid request.",
                    'is_ok': False
                },
                status=400
            )

        item = get_object_or_404(WatchItem, pk=pk)
        item.is_watched = is_watched
        item.save()

        return JsonResponse(
            {
                'message': "watch status successfully updated.",
                'is_ok': True
            },
            status=200

        )
    return JsonResponse({"error": "Method Not Allowed"}, status=405)


def delete_view(request, pk):
    item = get_object_or_404(WatchItem, pk=pk)
    return render(request, 'delete_item.html', {'item': item})

def delete_api_view(request, pk: int) -> JsonResponse:
    if request.method != "DELETE":
        return JsonResponse({"error": "Method Not Allowed"}, status=405)
    try:
        obj = WatchItem.objects.get(pk=pk)
    except WatchItem.DoesNotExist:
        return JsonResponse(
            {
                "message": "Item not found."
            },
            status=404
        )
    obj.delete()
    return JsonResponse({}, status=204)






