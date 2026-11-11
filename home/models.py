from django.db import models
from wagtail.models import Page
from wagtail.snippets.models import register_snippet
from wagtail.admin.panels import FieldPanel
from wagtail.fields import RichTextField

# ==============================================================================
# 1. SNIPPET : LES TECHNOLOGIES IA (Éléments réutilisables dans Wagtail)
# ==============================================================================
@register_snippet
class TechnologieIA(models.Model):
    # Liste des choix de handicap pour le menu déroulant
    HANDICAP_CHOICES = [
        ('Handicap Visuel', 'Handicap Visuel'),
        ('Handicap Auditif', 'Handicap Auditif'),
        ('Handicap Moteur', 'Handicap Moteur'),
        ('Handicap Cognitif', 'Handicap Cognitif'),
    ]

    # Champs de saisie dans l'administration Wagtail pour chaque outil IA
    nom = models.CharField("Nom de la technologie", max_length=100)
    categorie = models.CharField(
        "Type de Handicap", 
        max_length=50, 
        choices=HANDICAP_CHOICES,
        default='Handicap Visuel'
    )
    description = models.TextField("Description courte")
    lien_officiel = models.URLField("Lien officiel / Fiche", blank=True)
    image = models.ForeignKey(
        'wagtailimages.Image',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='+',
        verbose_name="Illustration"
    )

    # Attribution automatique d'une couleur au badge selon le handicap
    @property
    def badge_couleur(self):
        couleurs = {
            'Handicap Visuel': 'bg-primary text-white',   # Bleu
            'Handicap Auditif': 'bg-success text-white',  # Vert
            'Handicap Moteur': 'bg-warning text-dark',    # Jaune
            'Handicap Cognitif': 'bg-info text-dark',     # Cyan
        }
        return couleurs.get(self.categorie, 'bg-secondary text-white')

    # Affichage des formulaires de saisie dans l'Admin Wagtail
    panels = [
        FieldPanel('nom'),
        FieldPanel('categorie'),
        FieldPanel('description'),
        FieldPanel('lien_officiel'),
        FieldPanel('image'),
    ]

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Technologie IA"
        verbose_name_plural = "Technologies IA"


# ==============================================================================
# 2. PAGE D'ACCUEIL (HomePage)
# ==============================================================================
class HomePage(Page):
    # ==========================================================================
    # CHAMPS DU HERO BANNER (Administrables dans Wagtail)
    # ==========================================================================
    
    # Champ texte court pour le titre de la bannière
    intro_title = models.CharField(max_length=255, blank=True, verbose_name="Titre du Hero")
    
    # Champ texte long pour la description d'introduction
    
    intro_text = RichTextField(blank=True, verbose_name="Texte du Hero Banner")
    
    # Champ Image lié au sélecteur d'images de Wagtail
    banner_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image de la bannière"
    )

    # --- BLOC 2 : GENÈSE DU PROJET (Champs modifiables dans Wagtail) ---
    genese_title = models.CharField(max_length=255, blank=True, verbose_name="Titre Genèse")
    genese_text = RichTextField(blank=True, verbose_name="Texte Présentation & Genèse")
    genese_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image de la Genèse"
    )

    # Affichage des champs dans le panneau de modification de Wagtail
    content_panels = Page.content_panels + [
        FieldPanel('intro_title'),
        FieldPanel('intro_text'),
        FieldPanel('banner_image'),
        FieldPanel('genese_title'),
        FieldPanel('genese_text'),
        FieldPanel('genese_image'),
    ]

    # Méthode qui envoie la liste des Snippets au template HTML
    def get_context(self, request):
        context = super().get_context(request)
        context['technologies'] = TechnologieIA.objects.all()
        return context
