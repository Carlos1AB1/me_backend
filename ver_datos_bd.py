#!/usr/bin/env python
"""
Script para ver todos los datos en la base de datos
Ejecutar en PythonAnywhere: python ver_datos_bd.py
"""

import os
import sys
import django

# Configurar Django
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_backend.settings')
django.setup()

from skills.models import Skill, SkillCategory
from projects.models import Project, ProjectImage
from services.models import Service, ServiceCategory
from blog.models import BlogPost
from django.contrib.auth import get_user_model

User = get_user_model()

def print_separator(title):
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80)

def print_skills():
    print_separator("SKILLS")
    skills = Skill.objects.all().order_by('order')
    print(f"Total: {skills.count()}")
    print()
    
    for skill in skills:
        print(f"📦 {skill.name}")
        print(f"   ID: {skill.id}")
        print(f"   Categoría: {skill.category.name if skill.category else 'Sin categoría'}")
        print(f"   Nivel: {skill.level}")
        print(f"   Featured: {'✅' if skill.is_featured else '❌'}")
        print(f"   Imagen (archivo): {skill.image.name if skill.image else 'Sin archivo'}")
        print(f"   Imagen URL: {skill.image_url if skill.image_url else 'Sin URL'}")
        print(f"   Sub-imagen (archivo): {skill.sub_image.name if skill.sub_image else 'Sin archivo'}")
        print(f"   Sub-imagen URL: {skill.sub_image_url if skill.sub_image_url else 'Sin URL'}")
        print()

def print_categories():
    print_separator("CATEGORÍAS DE SKILLS")
    categories = SkillCategory.objects.all().order_by('order')
    print(f"Total: {categories.count()}")
    print()
    
    for cat in categories:
        count = cat.skills.count()
        print(f"📁 {cat.name} ({count} skills)")
        print(f"   ID: {cat.id}")
        print(f"   Orden: {cat.order}")
        print()

def print_projects():
    print_separator("PROJECTS")
    projects = Project.objects.all().order_by('-priority', '-created_at')
    print(f"Total: {projects.count()}")
    print()
    
    for proj in projects:
        print(f"🚀 {proj.title}")
        print(f"   ID: {proj.id}")
        print(f"   Slug: {proj.slug}")
        print(f"   Status: {proj.status}")
        print(f"   Featured: {'✅' if proj.featured else '❌'}")
        print(f"   Priority: {proj.priority}")
        print(f"   GitHub: {proj.github_url if proj.github_url else 'N/A'}")
        print(f"   Live URL: {proj.live_url if proj.live_url else 'N/A'}")
        
        # Imágenes del proyecto
        images = proj.images.all().order_by('order')
        if images:
            print(f"   📸 Imágenes ({images.count()}):")
            for img in images:
                if img.image_url:
                    print(f"      - URL: {img.image_url}")
                elif img.image:
                    print(f"      - Archivo: {img.image.name}")
                else:
                    print(f"      - Sin imagen")
        else:
            print(f"   📸 Sin imágenes")
        print()

def print_services():
    print_separator("SERVICES")
    services = Service.objects.all().order_by('order')
    print(f"Total: {services.count()}")
    print()
    
    for serv in services:
        print(f"💼 {serv.title}")
        print(f"   ID: {serv.id}")
        print(f"   Slug: {serv.slug}")
        print(f"   Categoría: {serv.category.name if serv.category else 'Sin categoría'}")
        print(f"   Precio: {serv.get_price_display()}")
        print(f"   Featured: {'✅' if serv.is_featured else '❌'}")
        print(f"   Active: {'✅' if serv.is_active else '❌'}")
        print(f"   Imagen (archivo): {serv.image.name if serv.image else 'Sin archivo'}")
        print(f"   Imagen URL: {serv.image_url if serv.image_url else 'Sin URL'}")
        print()

def print_blog():
    print_separator("BLOG POSTS")
    posts = BlogPost.objects.all().order_by('-published_at')
    print(f"Total: {posts.count()}")
    print()
    
    for post in posts:
        print(f"📝 {post.title}")
        print(f"   ID: {post.id}")
        print(f"   Slug: {post.slug}")
        print(f"   Status: {post.status}")
        print(f"   Publicado: {post.published_at if post.published_at else 'No publicado'}")
        print(f"   Imagen destacada: {post.featured_image.name if post.featured_image else 'Sin imagen'}")
        print()

def print_users():
    print_separator("USUARIOS")
    users = User.objects.all()
    print(f"Total: {users.count()}")
    print()
    
    for user in users:
        print(f"👤 {user.username}")
        print(f"   Email: {user.email}")
        print(f"   Staff: {'✅' if user.is_staff else '❌'}")
        print(f"   Superuser: {'✅' if user.is_superuser else '❌'}")
        print(f"   Activo: {'✅' if user.is_active else '❌'}")
        print()

def print_summary():
    print_separator("RESUMEN")
    print(f"Skills: {Skill.objects.count()}")
    print(f"Categorías de Skills: {SkillCategory.objects.count()}")
    print(f"Projects: {Project.objects.count()}")
    print(f"Imágenes de Projects: {ProjectImage.objects.count()}")
    print(f"Services: {Service.objects.count()}")
    print(f"Categorías de Services: {ServiceCategory.objects.count()}")
    print(f"Blog Posts: {BlogPost.objects.count()}")
    print(f"Usuarios: {User.objects.count()}")
    print()

def print_image_status():
    print_separator("ESTADO DE IMÁGENES")
    
    # Skills
    skills_with_file = Skill.objects.exclude(image='').count()
    skills_with_url = Skill.objects.exclude(image_url='').exclude(image_url__isnull=True).count()
    skills_without = Skill.objects.filter(image='', image_url__isnull=True).count() + \
                     Skill.objects.filter(image='', image_url='').count()
    
    print("Skills:")
    print(f"  - Con archivo subido: {skills_with_file}")
    print(f"  - Con URL externa: {skills_with_url}")
    print(f"  - Sin imagen: {skills_without}")
    print()
    
    # Projects
    proj_images_file = ProjectImage.objects.exclude(image='').count()
    proj_images_url = ProjectImage.objects.exclude(image_url='').exclude(image_url__isnull=True).count()
    
    print("Projects:")
    print(f"  - Imágenes con archivo: {proj_images_file}")
    print(f"  - Imágenes con URL: {proj_images_url}")
    print()
    
    # Services
    serv_with_file = Service.objects.exclude(image='').count()
    serv_with_url = Service.objects.exclude(image_url='').exclude(image_url__isnull=True).count()
    
    print("Services:")
    print(f"  - Con archivo subido: {serv_with_file}")
    print(f"  - Con URL externa: {serv_with_url}")
    print()

if __name__ == '__main__':
    print("\n")
    print("🔍" * 40)
    print("     DATOS EN LA BASE DE DATOS DE PYTHONANYWHERE")
    print("🔍" * 40)
    
    print_summary()
    print_image_status()
    print_categories()
    print_skills()
    print_projects()
    print_services()
    print_blog()
    print_users()
    
    print_separator("FIN DEL REPORTE")
    print()

