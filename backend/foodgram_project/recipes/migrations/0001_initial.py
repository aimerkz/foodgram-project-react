# Generated by Django 2.2.16 on 2022-07-11 14:43

import colorfield.fields
from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.db.models.expressions


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ingredient',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название ингредиента')),
                ('measurement_unit', models.CharField(max_length=200, verbose_name='Единица измерения')),
            ],
            options={
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
                'ordering': ['name'],
            },
        ),
        migrations.CreateModel(
            name='IngredientRecipes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Количество не может быть меньше 1')], verbose_name='Количество')),
                ('ingredients', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe_ingredients', to='recipes.Ingredient')),
            ],
            options={
                'verbose_name': 'Ингредиент рецепта',
                'verbose_name_plural': 'Ингредиенты рецепта',
            },
        ),
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Название рецепта')),
                ('image', models.ImageField(upload_to='recipes/images/', verbose_name='Ссылка на изображение')),
                ('text', models.TextField(verbose_name='Описание рецепта')),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('cooking_time', models.IntegerField(validators=[django.core.validators.MinValueValidator(1, 'Время приготовления не может быть меньше 1 минуты')], verbose_name='Время приготовления в мин')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes', to=settings.AUTH_USER_MODEL, verbose_name='Автор')),
                ('ingredients', models.ManyToManyField(related_name='recipes', through='recipes.IngredientRecipes', to='recipes.Ingredient', verbose_name='Список ингредиентов')),
            ],
            options={
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True, verbose_name='Название тега')),
                ('color', colorfield.fields.ColorField(default='#000000', image_field=None, max_length=7, samples=None, verbose_name='Код цвета')),
                ('slug', models.SlugField(max_length=200, unique=True, verbose_name='Слаг тега')),
            ],
            options={
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='ShoppingList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список покупок',
                'verbose_name_plural': 'Списки покупок',
            },
        ),
        migrations.CreateModel(
            name='RecipeTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт')),
                ('tag', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Tag', verbose_name='Тег')),
            ],
            options={
                'verbose_name': 'Тег рецепта',
                'verbose_name_plural': 'Теги рецепта',
            },
        ),
        migrations.CreateModel(
            name='RecipeFavorites',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recipes.Recipe', verbose_name='Рецепт')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Пользователь')),
            ],
            options={
                'verbose_name': 'Список избранного',
                'verbose_name_plural': 'Списки избранного',
            },
        ),
        migrations.AddField(
            model_name='recipe',
            name='tag',
            field=models.ManyToManyField(related_name='recipes', through='recipes.RecipeTag', to='recipes.Tag', verbose_name='Список тегов'),
        ),
        migrations.AddField(
            model_name='ingredientrecipes',
            name='recipes',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipes_ingredients', to='recipes.Recipe'),
        ),
        migrations.CreateModel(
            name='Follow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='following', to=settings.AUTH_USER_MODEL, verbose_name='Автор рецепта')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='follower', to=settings.AUTH_USER_MODEL, verbose_name='Подписчик')),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.AddConstraint(
            model_name='shoppinglist',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_list'),
        ),
        migrations.AddConstraint(
            model_name='recipefavorites',
            constraint=models.UniqueConstraint(fields=('user', 'recipe'), name='unique_recipe_favorites'),
        ),
        migrations.AddConstraint(
            model_name='ingredientrecipes',
            constraint=models.UniqueConstraint(fields=('recipe', 'ingredients'), name='unique_ingredients'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(fields=('user', 'author'), name='unique_follow'),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.CheckConstraint(check=models.Q(_negated=True, user=django.db.models.expressions.F('author')), name='user_is_not_author'),
        ),
    ]
