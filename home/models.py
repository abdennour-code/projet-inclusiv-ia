from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField


@register_snippet
class TechnologieIA(models.Model):
    HANDICAP_CHOICES = [
        ('Handicap Visuel', 'Handicap Visuel'),
        ('Handicap Auditif', 'Handicap Auditif'),
        ('Handicap Moteur', 'Handicap Moteur'),
        ('Handicap Cognitif', 'Handicap Cognitif'),
    ]

    nom = models.CharField("Nom de la technologie", max_length=100)
    categorie = models.CharField(
        "Type de Handicap", 
        max_length=50, 
        choices=HANDICAP_CHOICES,
        default='Handicap Visuel'
    )
    description = models.TextField("Description courte")
    
    lien_officiel = models.URLField(
        "Lien officiel / Fiche", 
        blank=True, 
        help_text="Adresse du site web officiel de la technologie"
    )
    
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Illustration"
    )

    # Attribution automatique de la couleur basée sur le handicap choisi
    @property
    def badge_couleur(self):
        couleurs = {
            'Handicap Visuel': 'bg-primary text-white',   # Bleu
            'Handicap Auditif': 'bg-success text-white',  # Vert
            'Handicap Moteur': 'bg-warning text-dark',    # Jaune
            'Handicap Cognitif': 'bg-info text-dark',     # Cyan
        }
        return couleurs.get(self.categorie, 'bg-secondary text-white')

    panels = [
        FieldPanel('nom'),
        FieldPanel('categorie'),  # Menu déroulant simple et guidé !
        FieldPanel('description'),
        FieldPanel('lien_officiel'),
        FieldPanel('image'),
    ]

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Technologie IA"
        verbose_name_plural = "Technologies IA"


class HomePage(Page):
    intro_title = models.CharField(max_length=255, blank=True)
    intro_text = models.TextField(blank=True)
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+'
    )

    content_panels = Page.content_panels + [
        FieldPanel('intro_title'),
        FieldPanel('intro_text'),
        FieldPanel('banner_image'),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context['technologies'] = TechnologieIA.objects.all()
        return context