from django.db import models
from wagtail.models import Page
from wagtail.fields import RichTextField
from wagtail.admin.panels import (
    FieldPanel, 
    InlinePanel, 
    FieldRowPanel, 
    MultiFieldPanel
)
from modelcluster.fields import ParentalKey
from wagtail.contrib.forms.models import AbstractEmailForm, AbstractFormField
from wagtail.contrib.forms.panels import FormSubmissionsPanel


# ==========================================
# 1. PAGES DOSSIERS (Nos Dossiers & Articles)
# ==========================================

class DossiersIndexPage(Page):
    intro = RichTextField(blank=True, verbose_name="Introduction de la page Nos Dossiers")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
    ]

    def get_context(self, request):
        # Récupère l'ensemble des sous-pages 'DossierPage' publiées rattachées à cet index
        context = super().get_context(request)
        context['dossiers'] = DossierPage.objects.child_of(self).live()
        return context


class DossierPage(Page):
    # Choix restreints correspondant aux 4 piliers technologiques du projet Inclusiv'IA
    CATEGORIE_CHOICES = [
        ('moteur', 'Handicap Moteur'),
        ('auditif', 'Handicap Auditif'),
        ('visuel', 'Handicap Visuel'),
        ('cognitif', 'Handicap Cognitif'),
    ]

    # Champ de sélection de la thématique
    categorie = models.CharField(
        max_length=50,
        choices=CATEGORIE_CHOICES,
        default='moteur',
        verbose_name="Thématique / Catégorie"
    )

    # Chapeau d'introduction affiché sur les cartes d'index et en début d'article
    chapeau = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Résumé court (Chapeau)"
    )

    # Clé étrangère vers l'image principale gérée par Wagtail
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image principale"
    )

    # Corps de l'article formaté via l'éditeur RichText
    body = RichTextField(blank=True, verbose_name="Contenu détaillé du dossier")

    # Champ de texte enrichi obligatoire réservé au référencement des sources et études
    bibliographie = RichTextField(
        verbose_name="Bibliographie & Sources"
    )

    # Panneaux de saisie affichés dans l'interface d'administration Wagtail
    content_panels = Page.content_panels + [
        FieldPanel('categorie'),
        FieldPanel('chapeau'),
        FieldPanel('main_image'),
        FieldPanel('body'),
        FieldPanel('bibliographie'),
    ]


# ==========================================
# 2. PAGE CONTACT & FORMULAIRE D'AUDIT
# ==========================================

class FormField(AbstractFormField):
    page = ParentalKey('ContactPage', on_delete=models.CASCADE, related_name='form_fields')


class ContactPage(AbstractEmailForm):
    intro = RichTextField(blank=True, verbose_name="Introduction")
    thank_you_text = RichTextField(blank=True, verbose_name="Message de remerciement")

    content_panels = AbstractEmailForm.content_panels + [
        FormSubmissionsPanel(),
        FieldPanel('intro'),
        InlinePanel('form_fields', label="Champs du formulaire"),
        FieldPanel('thank_you_text'),
        MultiFieldPanel([
            FieldRowPanel([
                FieldPanel('from_address', classname="col6"),
                FieldPanel('to_address', classname="col6"),
            ]),
            FieldPanel('subject'),
        ], "Configuration de l'email"),
    ]


# ==========================================
# 3. PAGE MENTIONS LÉGALES ET RGPD
# ==========================================

class RgpdPage(Page):
    """
    Page éditable dans Wagtail Admin contenant les Mentions Légales 
    et la Politique de Confidentialité (Conforme RGPD & CNIL)
    """
    intro = RichTextField(blank=True, verbose_name="Introduction / Chapeau")
    body = RichTextField(blank=True, verbose_name="Texte officiel des mentions légales & RGPD")

    content_panels = Page.content_panels + [
        FieldPanel('intro'),
        FieldPanel('body'),
    ]