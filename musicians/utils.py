from uuid import uuid4


def dynamic_upload_path(instance, filename):

    ext = filename.split('.')[-1]
    filename = f"{uuid4()}.{ext}"

    model_name = instance.__class__.__name__

    if model_name == "MusicProject":
        project_id = instance.id
        return f"music_project/{project_id}/profile/{filename}"

    if model_name == "MusicProjectImage":
        project_id = instance.music_project.id
        return f"music_project/{project_id}/gallery/{filename}"

    if model_name == "Discography":
        project_id = instance.music_project.id
        return f"music_project/{project_id}/discography_covers/{filename}"

    return f"misc/{filename}"
