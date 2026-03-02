from datetime import timedelta
from django.db import models
from django.utils import timezone
from django.utils.timezone import now
from django.contrib.auth import get_user_model
from django.views.generic.base import logger
from django.core.signing import BadSignature, SignatureExpired, TimestampSigner
from services.models import Attribute, Category, Item, PricingInterval, ServiceMode, SpecificService
from core.models import Country, MusicalGenreTag, Language, Instrument
from musicians.utils import dynamic_upload_path
from safedelete.models import SafeDeleteModel


User = get_user_model()


class MusicProjectType(models.Model):
    name = models.CharField(max_length=150, unique=True)
    display_name = models.CharField(max_length=150, unique=True)

    def __str__(self):
        return self.name

class TopicArtist(models.Model):
    name = models.TextField()
    individual = models.BooleanField(default=False)
    def __str__(self):
        return self.name

class CategoryMusic(models.Model):
    name = models.CharField(max_length=230, unique=True)
    reference = models.CharField(max_length=230)
    image = models.ImageField(upload_to=dynamic_upload_path)
    music_genre_tags = models.ManyToManyField(MusicalGenreTag, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    topics = models.ManyToManyField(TopicArtist, blank=True)
    orderservices = models.ManyToManyField("orders.OrderServiceType", blank=True)
    instruments = models.ManyToManyField(Instrument, blank=True)
    typemusictext = models.CharField(max_length=150, default="Intermedio")

    TYPE_INPUT_CHOICES = [
        ('select', 'Selección única'),
        ('multiple', 'Selección multiple'),
    ]
    type_input = models.CharField(max_length=20, choices=TYPE_INPUT_CHOICES, default='select', null=True)

    TYPE_MUSICIAN_CHOICES = [
        ('vocalist', 'Vocalistas'),
        ('instrumentalist', 'Instrumetalista'),
        ('multiinstrumentalist', 'Multi Instrumetalista'),
        ('djproductor', 'DJ Productor'),
    ]
    type_musician = models.CharField(max_length=30, choices=TYPE_MUSICIAN_CHOICES, default='select', null=True)

class MusicProjectImage(models.Model):
    music_project = models.ForeignKey(
        'MusicProject',
        on_delete=models.CASCADE,
        related_name='gallery'
    )
    image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)
    caption = models.CharField(max_length=255, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    thumbnail_position = models.CharField(max_length=12, blank=True, null=True)

    def __str__(self):
        return f"Image for {self.music_project.name}"


class AvailabilityInfoDaySchedule(models.Model):
    VIRTUAL = 'virtual'
    ON_SITE = 'on_site'

    MODALITIES = [
        (VIRTUAL, 'Virtual'),
        (ON_SITE, 'On Site'),
    ]

    availability = models.ForeignKey('AvailabilityInfo', on_delete=models.CASCADE, related_name="day_schedule")
    date = models.DateField()

    modality = models.CharField(max_length=50, choices=MODALITIES)


class AvailabilityInfoTimeSchedule(models.Model):
    MONDAY = 'monday'
    TUESDAY = 'tuesday'
    WEDNESDAY = 'wednesday'
    THURSDAY = 'thursday'
    FRIDAY = 'friday'
    SATURDAY = 'saturday'
    SUNDAY = 'sunday'

    WEEK_DAYS = [
        (MONDAY, 'Lunes'),
        (TUESDAY, 'Martes'),
        (WEDNESDAY, 'Miércoles'),
        (THURSDAY, 'Jueves'),
        (FRIDAY, 'Viernes'),
        (SATURDAY, 'Sábado'),
        (SUNDAY, 'Domingo'),
    ]

    availability = models.ForeignKey('AvailabilityInfo', on_delete=models.CASCADE, related_name="time_schedule")

    day = models.CharField(max_length=10, choices=WEEK_DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()


class AvailabilityInfo(models.Model):
    music_project = models.OneToOneField(
        'MusicProject',
        on_delete=models.CASCADE,
        related_name='availability_info'
    )

class MusicProject(SafeDeleteModel):

    name = models.CharField(max_length=150)
    slug = models.SlugField(default="", null=True, unique=True)
    description = models.TextField(blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="projects")
    project_type = models.ForeignKey(MusicProjectType, on_delete=models.CASCADE, related_name="project_types")
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name="member_projects", blank=True)
    number_courses = models.IntegerField(default=0, null=True, blank=True)
    number_students = models.IntegerField(default=0, null=True, blank=True)

    # feedback and reviews
    score = models.FloatField(default=0, null=True, blank=True)
    feedback_count = models.IntegerField(default=0, null=True, blank=True)

    birth_date = models.DateField(null=True, blank=True)
    phone_number = models.CharField(max_length=50, blank=True, null=True)
    country = models.ForeignKey(Country, on_delete=models.SET_NULL, null=True, blank=True)

    # Manager information
    manager_name = models.CharField(max_length=150, blank=True, null=True)
    manager_number = models.CharField(max_length=50, blank=True, null=True)

    # General information
    biography = models.TextField(blank=True, null=True)
    profile_image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)
    cover_image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)
    years_of_experience = models.IntegerField(blank=True, null=True)
    music_genre_tags = models.ManyToManyField(MusicalGenreTag, blank=True)
    languages = models.ManyToManyField(Language, blank=True)
    topics = models.ManyToManyField(TopicArtist, blank=True)
    orderservices = models.ManyToManyField("orders.OrderServiceType", blank=True)
    instruments = models.ManyToManyField(Instrument, through="MusicProjectInstrument", blank=True)
    categories = models.ManyToManyField(CategoryMusic, blank=True)
    service_categories = models.ManyToManyField("services.Category", blank=True, related_name="musicprojects")

    # profile completion state
    isProfileInfoCompleted = models.BooleanField(default=False)
    isVerificationStepsCompleted = models.BooleanField(default=False)
    isAvailabilityCompleted = models.BooleanField(default=False)

    isInstrumentsCompleted = models.BooleanField(default=False)
    isServicesCompleted = models.BooleanField(default=False)

    is_blocked = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        """ Generate number order """
        if not self.slug:
            today = now().strftime("%Y%m%d")
            last_slug = MusicProject.objects.filter(slug__startswith=f"MUSIC-{today}").order_by('-id').first()
            if last_slug:
                last_number = int(last_slug.slug.split('-')[-1]) + 1
            else:
                last_number = 1
            self.slug = f"MUSIC-{today}-{last_number:05d}"  # Format MUSIC-YYYYMMDD-00001

        super().save(*args, **kwargs)


    def update_score(self):
        """
        Recalculate and update the score as a mean of the feedbacks received
        """
        result = self.feedbacks.aggregate(
            avg_score=models.Avg('score'),
            count=models.Count('score'),
        )

        self.score = result['avg_score'] or 0
        self.feedback_count = result['count']
        self.save(update_fields=['score', 'feedback_count'])


    def __str__(self):
        return self.name



class Discography(models.Model):
    ALBUM = 'ALBUM'
    EP = 'EP'

    TYPE_CHOICES = [
        (ALBUM, 'Album'),
        (EP, 'EP'),
    ]

    music_project = models.ForeignKey(
        MusicProject,
        on_delete=models.CASCADE,
        related_name='discography'
    )
    title = models.CharField(max_length=200, null=True, blank=True)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)

    # for documentation purposes, the cover image used to be a file. Now, it will be just a URL from the Spotify API
    # cover_image = models.ImageField(upload_to=dynamic_upload_path, null=True, blank=True)

    cover_image = models.URLField(null=True, blank=True)
    url_link = models.URLField()
    year_of_release = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return f"{self.title} - {self.music_project.name}"


class Single(models.Model):
    music_project = models.ForeignKey(
        MusicProject,
        on_delete=models.CASCADE,
        related_name='singles'
    )
    album = models.ForeignKey(Discography, on_delete=models.CASCADE, related_name='singles', null=True, blank=True)
    title = models.CharField(max_length=200)
    url_link = models.URLField()

    def __str__(self):
        return f"{self.title} - {self.music_project.name}"

class InviteMemberBand(models.Model):

    STATUS_ACCEPTED = 'accepted'
    STATUS_CANCELED = 'canceled'
    STATUS_INPROCESS = 'in_process'

    music_project = models.ForeignKey(
        MusicProject,
        on_delete=models.CASCADE,
        related_name='invitemusicproject'
    )
    invited_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_invitations", null=True, blank=True)
    inviter = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name="sent_invitations")
    email = models.CharField(max_length=200)
    STATUS_CHOICES = [
        (STATUS_ACCEPTED, 'Aceptado'),
        (STATUS_CANCELED, 'Cancelado'),
        (STATUS_INPROCESS, 'En proceso'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=STATUS_INPROCESS)
    message = models.TextField(null=True, blank=True, help_text="Escriba un mensaje personalizado para el invitado.")

    expires_at = models.DateTimeField()
    responded_at = models.DateTimeField(default=None, null=True, blank=True)
    sent_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):

        if not self.invited_user_id:
            try:
                self.invited_user = User.objects.get(email=self.email)
            except User.DoesNotExist:
                pass

        self.expires_at = timezone.now() + timedelta(days=7)
        super().save(*args, **kwargs)

    def generate_token(self):
        """
        Generate a secure token with the invitee email
        """
        signer = TimestampSigner()
        value = f"{self.id}:{self.email}"
        return signer.sign(value)

    @classmethod
    def verify_token(cls, token):
        """
        Verify the token generated and parse it.
        Returns an invitation instance, and an error string
        """

        signer = TimestampSigner()

        try:
            value = signer.unsign(token, max_age=7 * 24 * 60 * 60)
            id, email = value.split(':', 1)

            invitation = cls.objects.get(id=id)

            if invitation.status != cls.STATUS_INPROCESS:
                return None, f"The invitation has already been {invitation.status}."

            if invitation.email != email:
                return None, "The token is not valid"

            if invitation.is_expired:
                return None, "The invitation has expired"

            return invitation, None
        except SignatureExpired:
            return None, "The invitation has expired"
        except BadSignature:
            return None, "The token is not valid"
        except cls.DoesNotExist:
            return None, "The invitation does not exist"
        except ValueError:
            return None, "The token is not valid"

    @property
    def is_expired(self):
        return timezone.now() > self.expires_at

    def expire(self):
        self.status = self.STATUS_CANCELED
        self.responded_at = timezone.now()
        self.save()

    def accept(self, user=None, email=None):
        if self.is_expired:
            raise ValueError("El enlace ha expirado.")

        if self.status != self.STATUS_INPROCESS:
            raise ValueError("El enlace ya ha sido aceptado.")

        if user and email:
            raise ValueError("you can only specify either a user or an email")

        if email:
            user = User.objects.filter(email=email).first()

        accepting_user = user or self.invited_user
        if not accepting_user:
            raise ValueError("El usuario que acepta el enlace no es válido.")

        # add the current user to the band
        self.music_project.members.add(accepting_user)

        self.status = self.STATUS_ACCEPTED
        self.responded_at = timezone.now()
        self.save()

    def decline(self):
        if self.status != self.STATUS_INPROCESS:
            raise ValueError("El enlace ya ha sido aceptado.")

        self.status = self.STATUS_CANCELED
        self.save()

    class Meta:
        unique_together = ('music_project', 'email', 'status')
        # optimization time!
        indexes = [
            models.Index(fields=['email', 'status']),
            models.Index(fields=['expires_at']),
        ]

class MusicProjectInstrument(models.Model):
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE)
    instrument = models.ForeignKey(Instrument, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    price_per_instrument = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)

    brand = models.CharField(max_length=100, null=True, blank=True)
    model = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        unique_together = ('music_project', 'instrument')

class InstrumentSet(models.Model):
    instrument_set_name = models.CharField(max_length=150)
    # the instruments belonging to this instrument set must also belong to the music project beforehand
    instruments_in_current_set = models.ManyToManyField(
        MusicProjectInstrument,
        related_name="instrument_set",
        through="MusicProjectInstrumentInstrumentSet", # relationship for the quantity of each instrument
        blank=True
    )
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE, blank=True, related_name="instrument_sets")

    @property
    def calculated_total_price(self):
        """
        Calculate total price by adding the individual prices of each instrument
        """
        return sum(
            [mp.quantity_for_set * mp.music_project_instrument.price_per_instrument
            for mp in self.musicprojectinstrumentinstrumentset_set.all()]
        )

    def __str__(self):
        return self.instrument_set_name

class MusicProjectInstrumentInstrumentSet(models.Model):
    music_project_instrument = models.ForeignKey(MusicProjectInstrument, on_delete=models.CASCADE)
    instrument_set = models.ForeignKey(InstrumentSet, on_delete=models.CASCADE)
    quantity_for_set = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('music_project_instrument', 'instrument_set')

    def save(self, *args, **kwargs):
        # only if it is a new record
        if self.pk is None:
            if self.music_project_instrument.quantity < self.quantity_for_set:
                raise ValueError("Not enough instruments to add to current set")
            self.music_project_instrument.quantity -= self.quantity_for_set
            self.music_project_instrument.save()
        else:  # updating existing record
            # we need to calculate the difference between new and old value of quantity
            old_instance = MusicProjectInstrumentInstrumentSet.objects.get(pk=self.pk)
            quantity_diff = self.quantity_for_set - old_instance.quantity_for_set

            if quantity_diff > 0:
                if self.music_project_instrument.quantity < quantity_diff:
                    raise ValueError("Not enough instruments available")
                self.music_project_instrument.quantity -= quantity_diff
            else:
                self.music_project_instrument.quantity += abs(quantity_diff)

            self.music_project_instrument.save()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        # Add the quantity back before deleting
        self.music_project_instrument.quantity += self.quantity_for_set
        self.music_project_instrument.save()
        super().delete(*args, **kwargs)


class MusicProjectService(models.Model):
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE, related_name="services")
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)

    # references to the taxonomy levels
    category = models.ForeignKey(Category, on_delete=models.CASCADE, to_field="name")
    item = models.ForeignKey(Item, on_delete=models.CASCADE, to_field="name", null=True)
    specific_service = models.ForeignKey(SpecificService, on_delete=models.CASCADE, related_name="musicprojects", to_field="name")
    extra_fields = models.JSONField(default=dict)

    # Data about the musician's service
    attribute = models.ForeignKey(Attribute, on_delete=models.CASCADE, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    modes = models.ManyToManyField(ServiceMode)

    selected_instrument_set = models.ForeignKey(InstrumentSet, on_delete=models.CASCADE, null=True, blank=True)

    # metadata about the service
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.music_project.name} - {self.title}"

class MusicProjectVideo(models.Model):
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE, related_name="videos")

    video_url = models.URLField()
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class MusicProjectVideoDraftStatus(models.TextChoices):
    INPROCESS = "INPROCESS", 'inprocess'
    ACCEPTED = "ACCEPTED", 'accepted'
    REJECTED = "REJECTED", 'rejected'


class MusicProjectVideoDraft(models.Model):
    """
    Draft for music videos. The administrator would have to review the links,
    upload the videos to the YouTube channel and then notify the users that their
    video has been published in the platform
    """
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE, related_name="video_drafts")

    video_url = models.URLField()
    caption = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    status = models.CharField(max_length=100, choices=MusicProjectVideoDraftStatus.choices, default=MusicProjectVideoDraftStatus.INPROCESS)
    feedback = models.TextField(blank=True, null=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    reviewed_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Video Draft for {self.music_project.name} - {self.video_url}"

    def review(self, status: MusicProjectVideoDraftStatus, feedback, reviewed_by):
        self.status = status
        self.feedback = feedback
        self.reviewed_by = reviewed_by
        self.reviewed_at = timezone.now()

        if self.status == MusicProjectVideoDraftStatus.ACCEPTED:
            # attach the video to the actual music project to be showed publically
            MusicProjectVideo.objects.create(
                music_project=self.music_project,
                video_url=self.video_url,
                caption=self.caption
            )

        self.save()

    @classmethod
    def get_pending_drafts(cls, music_project_id):
        return cls.objects.filter(
            status=MusicProjectVideoDraftStatus.INPROCESS
        ).filter(
            music_project_id=music_project_id
        )


class Feedback(models.Model):
    music_project = models.ForeignKey(MusicProject, on_delete=models.CASCADE, related_name="feedbacks")
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="feedbacks")
    score = models.PositiveIntegerField() # 1 through 5 stars
    feedback = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
