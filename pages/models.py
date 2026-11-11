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
        context = super().get_context(request)
        context['dossiers'] = DossierPage.objects.child_of(self).live()
        return context


class DossierPage(Page):
    chapeau = models.CharField(
        max_length=500, 
        blank=True, 
        verbose_name="Résumé court (Chapeau)"
    )
    main_image = models.ForeignKey(
        'wagtailimages.Image',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='+',
        verbose_name="Image principale"
    )
    body = RichTextField(blank=True, verbose_name="Contenu détaillé du dossier")

    content_panels = Page.content_panels + [
        FieldPanel('chapeau'),
        FieldPanel('main_image'),
        FieldPanel('body'),
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