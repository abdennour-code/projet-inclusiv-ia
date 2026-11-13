# Justification des Choix d'Optimisation SEO & Référencement

**Projet Chef d'Œuvre :** Inclusiv'IA – Média de l'IA au service de l'accessibilité et du handicap  
**Framework / CMS :** Wagtail (Python / Django)  
**Candidat :** Abdennour L.  
**Évaluation :** Épreuve E2 – Cas pratique d'optimisation (Accessibilité & SEO)

---

## 1. Titres SEO (`seo_title`) et Méta-descriptions (`search_description`)

### Problématique & Enjeu
Sans balises spécifiques, Google génère un titre brut et un extrait aléatoire dans les résultats de recherche (SERP), ce qui réduit le taux de clic (CTR). Pour **Inclusiv'IA**, média spécialisé, il est primordial de positionner des mots-clés stratégiques (*IA*, *accessibilité*, *handicap*, *autonomie*, *LSF*, *BCI*).

### Mise en œuvre
- **Dans l'administration Wagtail (onglet *Promote*) :**  
  Chaque page principale a été dotée d'un `seo_title` et d'une `search_description` uniques :
  - **Accueil (`/`) :**
    - *SEO title :* `Inclusiv'IA - Média de l'IA au service de l'accessibilité et du handicap`
    - *Search description :* `Découvrez les innovations technologiques et assistants IA (transcription LSF, vision par ordinateur, cobotique) favorisant l'autonomie et l'inclusion.`
  - **Nos Dossiers (`/nos-dossiers/`) :**
    - *SEO title :* `Nos Dossiers & Décryptages IA - Inclusiv'IA`
    - *Search description :* `Explorez nos enquêtes et comparatifs sur l'intelligence artificielle appliquée à l'accessibilité : handicap visuel, auditif, moteur et cognitif.`
  - **Contact (`/contact/`) :**
    - *SEO title :* `Contact & Demande d'Audit Accessibilité Web - Inclusiv'IA`
    - *Search description :* `Une question sur l'IA inclusive ou besoin d'un accompagnement en accessibilité numérique ? Contactez l'équipe Inclusiv'IA à Bègles.`
  - **Mentions Légales & RGPD (`/mentions-legales/`) :**
    - *SEO title :* `Mentions Légales & Protection des Données (RGPD) - Inclusiv'IA`
    - *Search description :* `Consultez les informations légales, la politique de confidentialité RGPD et les droits d'accès aux données du site Inclusiv'IA.`

- **Sensibilisation et guidage dans le back-office (`models.py`) :**  
  Ajout d'attributs `help_text` explicites sur les champs des modèles Wagtail (dans `models.py`) pour accompagner les éditeurs lors de la rédaction des contenus. Ces consignes intégrées garantissent que tout futur contributeur renseignera des meta-descriptions conformes aux exigences d'accessibilité et de SEO.

- **Sécurité Code (`base.html`) :**  
  Intégration d'un mécanisme de secours (*fallback*) dans la balise `<head>` : si une description venait à manquer sur un article, une description générique sur Inclusiv'IA est automatiquement injectée pour garantir un score Lighthouse maximal.

---

## 2. Structure et Hiérarchie Sémantique des Titres

### Problématique
Les robots d'indexation analysent la structure HTML pour identifier le sujet central. La présence de plusieurs `<h1>` ou des sauts de niveaux (ex. `<h2>` suivi d'un `<h4>`) perturbent la compréhension du contenu.

### Mise en œuvre
- Un **unique `<h1>`** est présent sur chaque template de page (le nom de la plateforme sur l'accueil, l'intitulé de la section sur les sous-pages, ou le titre de la fiche technologie).
- Les sous-titres dans le champ éditorial `RichTextField` de Wagtail ont été configurés en `<h2>` pour structurer logiquement les paragraphes de décryptage sans sauts de niveau.

---

## 3. Textes Alternatifs des Images (`alt`)

### Problématique
Les moteurs de recherche ne "voient" pas les images et les lecteurs d'écran (utilisés par les personnes déficientes visuelles) ont besoin d'une description textuelle explicite.

### Mise en œuvre
- Sur le modèle des fiches et des snippets d'outils d'assistance (Ava, IRIS, Kinova, Goblin Tools), le tag Wagtail `{% image page.photo fill-... alt=page.photo_alt %}` ou l'attribut `alt` personnalisé dans le CMS est systématiquement renseigné.
- Les descriptions apportent du contexte (ex: *"Application de sous-titrage instantané Ava utilisée lors d'une réunion"* plutôt qu'un texte générique *"Image 1"*).
- Les éléments graphiques purement décoratifs disposent d'un `alt=""` explicite afin d'être ignorés par les lecteurs d'écran sans créer d'erreur d'accessibilité.

---

## 4. Génération Dynamique du Plan de Site (`/sitemap.xml`)

### Problématique
Garantir l'exploration et l'indexation exhaustive de toutes les pages de l'arborescence Wagtail par Googlebot sans dépendre uniquement du maillage interne.

### Mise en œuvre
- Activation des modules `django.contrib.sitemaps` et `wagtail.contrib.sitemaps` dans `INSTALLED_APPS` (`base.py`).
- Branchement de la route d'URL `path('sitemap.xml', sitemap)` dans `urls.py`.
- Le fichier XML est généré en temps réel et liste dynamiquement l'accueil, les dossiers, les fiches thématiques et les pages institutionnelles avec leur date de dernière modification (`<lastmod>`).

---

## 5. Fichier d'Instruction aux Robots (`/robots.txt`)

### Problématique
Indiquer aux robots les zones à ne pas explorer et leur fournir le point d'entrée direct vers le plan de site.

### Mise en œuvre
- Implémentation d'une vue dédiée dans `urls.py` renvoyant le fichier texte aux robots :
  - `User-agent: *` (s'adresse à l'ensemble des crawlers).
  - `Disallow: /admin/` et `Disallow: /django-admin/` (sécurise et évite l'indexation inutile de l'interface d'administration back-office).
  - `Sitemap: http://localhost:8000/sitemap.xml` (pointe directement vers le plan de site XML).

---

## 6. Maîtrise du Poids des Images et Performance

### Problématique
Le temps de chargement d'une page impacte directement le positionnement Google (Core Web Vitals) et l'expérience utilisateur, particulièrement sur mobile.

### Mise en œuvre
- Utilisation systématique du filtre de redimensionnement dynamique de Wagtail (`{% image page.cover_image fill-800x600 %}`).
- Les images téléversées en haute résolution par les éditeurs sont automatiquement compressées et recadrées à la dimension exacte du conteneur d'affichage.

---

## 7. Vérification et Audit Chrome Lighthouse

### Résultats obtenus sur Chrome DevTools :
- **Score Accessibilité :** **100 / 100** (Validation RGAA, contrastes, navigation clavier, liens d'évitement).
- **Score SEO :** **100 / 100** (Validation des méta-descriptions, balises viewport, titre de document, `robots.txt` et `sitemap.xml`).