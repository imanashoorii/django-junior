from django.http import JsonResponse
from django.http.multipartparser import MultiPartParser

from musify.models import Music, Singer


def music_serializer(obj: Music) -> dict:
    return {
        "id": obj.id,
        "title": obj.title,
        "singer": {
            "id": obj.singer.id,
            "name": obj.singer.name,
        },
        "description": obj.description,
        "year": int(obj.year) if obj.year else None,
        "file": obj.file.url if obj.file else None
    }


def list_create_view(request):

    # =========================
    # GET /musics/
    # =========================
    if request.method == 'GET':

        title = request.GET.get('title')
        singer = request.GET.get('singer')
        year = request.GET.get('year')

        qs = Music.objects.all()

        if title:
            qs = qs.filter(title__icontains=title)

        if singer:
            qs = qs.filter(singer__name__icontains=singer)

        if year:
            qs = qs.filter(year=year)

        result = [music_serializer(music) for music in qs]

        return JsonResponse(
            result,
            safe=False,
            status=200
        )

    # =========================
    # POST /musics/
    # =========================
    if request.method == 'POST':

        text_data, file_data = MultiPartParser(
            request.META,
            request,
            request.upload_handlers
        ).parse()

        # Required fields
        if 'title' not in text_data or 'singer' not in text_data:
            return JsonResponse(
                {
                    "error": "Missing required fields."
                },
                status=400
            )

        # Singer name -> Title Case
        singer_name = text_data.get('singer').title()

        singer, created = Singer.objects.get_or_create(
            name=singer_name
        )

        music = Music.objects.create(
            title=text_data.get('title'),
            singer=singer,
            description=text_data.get('description'),
            year=text_data.get('year') or None,
            file=file_data.get('music_file')
        )

        return JsonResponse(
            music_serializer(music),
            status=201
        )

    # =========================
    # Invalid method
    # =========================
    return JsonResponse(
        {
            "error": "Method Not Allowed"
        },
        status=405
    )


def retrieve_update_delete_view(request, pk):

    # =========================
    # Check method
    # =========================
    if request.method not in ['GET', 'PUT', 'PATCH', 'DELETE']:
        return JsonResponse(
            {
                "error": "Method Not Allowed"
            },
            status=405
        )

    # =========================
    # Get Music
    # =========================
    try:
        music = Music.objects.get(pk=pk)

    except Music.DoesNotExist:
        return JsonResponse(
            {
                "error": "Music not found."
            },
            status=404
        )

    # =========================
    # GET /musics/<pk>/
    # =========================
    if request.method == 'GET':

        return JsonResponse(
            music_serializer(music),
            status=200
        )

    # =========================
    # PUT /musics/<pk>/
    # =========================
    if request.method == 'PUT':

        text_data, file_data = MultiPartParser(
            request.META,
            request,
            request.upload_handlers
        ).parse()

        # Only title and singer are required
        if 'title' not in text_data or 'singer' not in text_data:
            return JsonResponse(
                {
                    "error": "Missing required fields."
                },
                status=400
            )

        # PUT = full update
        music.title = text_data.get('title')

        # Optional fields
        music.description = text_data.get('description')
        music.year = text_data.get('year') or None

        # Singer
        singer_name = text_data.get('singer').title()

        singer, created = Singer.objects.get_or_create(
            name=singer_name
        )

        music.singer = singer

        # File
        # If a new file is provided -> replace old file
        # If no file is provided -> remove old file
        if 'music_file' in file_data:
            music.file = file_data.get('music_file')
        else:
            music.file = None

        music.save()

        return JsonResponse(
            {
                "message": "Music updated successfully.",
                "music": music_serializer(music)
            },
            status=200
        )

    # =========================
    # PATCH /musics/<pk>/
    # =========================
    if request.method == 'PATCH':

        text_data, file_data = MultiPartParser(
            request.META,
            request,
            request.upload_handlers
        ).parse()

        # Only update fields that were actually sent

        if 'title' in text_data:
            music.title = text_data.get('title')

        if 'description' in text_data:
            music.description = text_data.get('description')

        if 'year' in text_data:
            music.year = text_data.get('year') or None

        if 'singer' in text_data:
            singer_name = text_data.get('singer').title()

            singer, created = Singer.objects.get_or_create(
                name=singer_name
            )

            music.singer = singer

        # Only change the file if a new file was sent
        if 'music_file' in file_data:
            music.file = file_data.get('music_file')

        music.save()

        return JsonResponse(
            {
                "message": "Music updated successfully.",
                "music": music_serializer(music)
            },
            status=200
        )

    # =========================
    # DELETE /musics/<pk>/
    # =========================
    if request.method == 'DELETE':

        music.delete()

        return JsonResponse(
            {},
            status=204
        )