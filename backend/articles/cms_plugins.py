from django.utils.translation import pgettext_lazy
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse, NoReverseMatch
from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from backend.articles.models import Article
from backend.articles.models import ArticleLinkModel
from backend.articles.models import ArticleTeasersCMSPlugin


MODULE_NAME = pgettext_lazy('plugins', 'Articles')


def namespace_is_apphooked(namespace):
    from backend.articles.urls import DEFAULT_VIEW  # avoid circular import
    """
    Check if provided namespace has an app-hooked page.
    Returns True or False.
    """
    try:
        reverse('{0}:{1}'.format(namespace, DEFAULT_VIEW))
    except NoReverseMatch:
        return False
    return True


class NameSpaceCheckMixin(object):

    def render(self, context, instance, placeholder):
        # check if we have a valid app_config that is app hooked to a page.
        # so that we won't have a 500 error if page with that app hook
        # was deleted.
        if instance.app_config:
            namespace = instance.app_config.namespace
        else:
            namespace = ''

        if not namespace_is_apphooked(namespace):
            context['plugin_configuration_error'] = _(
                'There is an error in plugin configuration: selected '
                'config is not available. Please switch to edit mode and '
                'change plugin app_config settings to use valid config. '
                'Also note that the blog app should be used at least once '
                'as an apphook for that config.')

        return super().render(context, instance, placeholder)


class ArticleTeasersPlugin(NameSpaceCheckMixin, CMSPluginBase):
    """
    Acts as a base plugin for extending
    """
    model = ArticleTeasersCMSPlugin
    module = MODULE_NAME
    name = _("Article Teasers")
    render_template = 'articles/plugins/article-teasers.html'
    allow_children = False

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)

        if instance.app_config:
            namespace = instance.app_config.namespace
        else:
            namespace = ''
        if namespace == '' or context.get('plugin_configuration_error', False):
            articles = Article.objects.none()
        else:
            articles = Article.objects.filter(is_active=True)

        context['articles'] = articles
        context['articles_count'] = len(articles)
        return context


@plugin_pool.register_plugin
class LastTwoArticleTeasersPlugin(ArticleTeasersPlugin):
    module = MODULE_NAME
    name = "Last Two Articles Teaser"
    render_template = 'articles/plugins/last-two-articles-teasers.html'

    def render(self, context, instance, placeholder):
        base_context = super().render(context, instance, placeholder)

        context['articles'] = base_context.get('articles').order_by('-created_at')[:2]
        return context


@plugin_pool.register_plugin
class ArticleLinkPlugin(CMSPluginBase):
    model = ArticleLinkModel
    module = MODULE_NAME
    name = _('News Article Link')
    render_template = 'articles/plugins/link-plugin.html'
    allow_children = False
    text_enabled = True

    def render(self, context, instance, placeholder):
        context = super().render(context, instance, placeholder)
        return context
