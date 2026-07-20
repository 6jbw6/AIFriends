import django.db.models.deletion
import web.models.character
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0009_voice_character_voice'),
    ]

    operations = [
        migrations.AddField(
            model_name='voice',
            name='owner',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='web.userprofile'),
        ),
        migrations.AddField(
            model_name='voice',
            name='audio',
            field=models.FileField(blank=True, null=True, upload_to=web.models.character.voice_audio_upload_to),
        ),
    ]
