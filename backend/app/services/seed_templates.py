"""
Seed built-in templates into the database.
Run once on startup if templates table is empty.
"""
from sqlalchemy.orm import Session
from app.models.template import Template

TEMPLATES = [
    # ─────────────────────────────────────────────
    # 1. Business Landing Page
    # ─────────────────────────────────────────────
    {
        "name": "Business Pro",
        "slug": "business-pro",
        "category": "business",
        "description": "صفحة هبوط احترافية للشركات والأعمال مع قسم Hero وخدمات وتواصل",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#2563eb",
            "secondary_color": "#1e40af",
            "accent_color": "#f59e0b",
            "background_color": "#ffffff",
            "text_color": "#1e293b",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "8px",
        },
        "thumbnail_url": "/static/templates/business-pro.png",
        "grapes_data": {
            "pages": [{
                "id": "main",
                "component": {
                    "type": "wrapper",
                    "components": [
                        {
                            "tagName": "nav",
                            "style": {"display": "flex", "align-items": "center", "justify-content": "space-between",
                                      "padding": "16px 48px", "background": "#ffffff", "box-shadow": "0 1px 3px rgba(0,0,0,.1)",
                                      "position": "sticky", "top": "0", "z-index": "100"},
                            "components": [
                                {"tagName": "div", "style": {"font-size": "1.5rem", "font-weight": "800", "color": "var(--primary, #2563eb)"},
                                 "content": "YourBrand"},
                                {"tagName": "div", "style": {"display": "flex", "gap": "32px"},
                                 "components": [
                                     {"tagName": "a", "attributes": {"href": "#services"}, "style": {"color": "#64748b", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "Services"},
                                     {"tagName": "a", "attributes": {"href": "#about"}, "style": {"color": "#64748b", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "About"},
                                     {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "8px 20px", "background": "var(--primary, #2563eb)", "color": "#fff", "border-radius": "6px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "600"}, "content": "Get Started"},
                                 ]},
                            ]
                        },
                        {
                            "tagName": "section",
                            "style": {"padding": "100px 48px", "background": "linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)", "text-align": "center"},
                            "components": [
                                {"tagName": "h1", "style": {"font-size": "3.5rem", "font-weight": "800", "color": "#0f172a", "margin": "0 0 20px", "line-height": "1.15"}, "content": "Grow Your Business<br>with Confidence"},
                                {"tagName": "p", "style": {"font-size": "1.25rem", "color": "#475569", "margin": "0 auto 40px", "max-width": "600px", "line-height": "1.7"}, "content": "We help businesses scale with proven strategies, cutting-edge technology, and dedicated support."},
                                {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center", "flex-wrap": "wrap"},
                                 "components": [
                                     {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "14px 36px", "background": "var(--primary, #2563eb)", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "Start Free Trial"},
                                     {"tagName": "a", "attributes": {"href": "#services"}, "style": {"display": "inline-block", "padding": "14px 36px", "background": "transparent", "color": "var(--primary, #2563eb)", "border": "2px solid var(--primary, #2563eb)", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "Learn More"},
                                 ]}
                            ]
                        },
                        {
                            "tagName": "section",
                            "attributes": {"id": "services"},
                            "style": {"padding": "80px 48px", "background": "#fff"},
                            "components": [
                                {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "margin": "0 0 12px", "color": "#0f172a"}, "content": "Our Services"},
                                {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 56px", "max-width": "500px"}, "content": "Everything you need to succeed in the digital world"},
                                {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "1100px", "margin": "0 auto"},
                                 "components": [
                                     *[{"tagName": "div", "style": {"padding": "32px", "border": "1px solid #e2e8f0", "border-radius": "12px", "transition": "box-shadow .2s"},
                                        "components": [
                                            {"tagName": "div", "style": {"font-size": "2rem", "margin-bottom": "16px"}, "content": icon},
                                            {"tagName": "h3", "style": {"font-size": "1.125rem", "font-weight": "700", "margin": "0 0 8px", "color": "#0f172a"}, "content": title},
                                            {"tagName": "p", "style": {"color": "#64748b", "font-size": ".9rem", "line-height": "1.6", "margin": "0"}, "content": desc},
                                        ]} for icon, title, desc in [
                                         ("🚀", "Growth Strategy", "Data-driven strategies that accelerate your business growth and market reach."),
                                         ("💡", "Innovation", "Cutting-edge solutions that keep you ahead of the competition."),
                                         ("🛡️", "Security", "Enterprise-grade security to protect your business and customer data."),
                                     ]]
                                 ]}
                            ]
                        },
                        {
                            "tagName": "section",
                            "style": {"padding": "80px 48px", "background": "var(--primary, #2563eb)", "text-align": "center"},
                            "components": [
                                {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "700", "color": "#fff", "margin": "0 0 16px"}, "content": "Ready to Get Started?"},
                                {"tagName": "p", "style": {"color": "#bfdbfe", "font-size": "1.125rem", "margin": "0 0 36px"}, "content": "Join thousands of businesses that trust us"},
                                {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "14px 40px", "background": "#fff", "color": "var(--primary, #2563eb)", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "Contact Us Today"},
                            ]
                        },
                        {
                            "tagName": "footer",
                            "style": {"background": "#0f172a", "color": "#94a3b8", "padding": "40px 48px", "text-align": "center"},
                            "components": [
                                {"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 YourBrand. All rights reserved."},
                            ]
                        }
                    ]
                }
            }],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 2. Creative Portfolio
    # ─────────────────────────────────────────────
    {
        "name": "Creative Portfolio",
        "slug": "creative-portfolio",
        "category": "portfolio",
        "description": "قالب بورتفوليو إبداعي للمصممين والمطورين والفنانين",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#8b5cf6",
            "secondary_color": "#6d28d9",
            "accent_color": "#ec4899",
            "background_color": "#0f172a",
            "text_color": "#f8fafc",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "12px",
        },
        "thumbnail_url": "/static/templates/portfolio.png",
        "grapes_data": {
            "pages": [{
                "id": "main",
                "component": {
                    "type": "wrapper",
                    "style": {"background": "#0f172a", "color": "#f8fafc", "font-family": "Inter, sans-serif"},
                    "components": [
                        {
                            "tagName": "nav",
                            "style": {"display": "flex", "align-items": "center", "justify-content": "space-between",
                                      "padding": "24px 48px", "background": "transparent"},
                            "components": [
                                {"tagName": "div", "style": {"font-size": "1.5rem", "font-weight": "800", "background": "linear-gradient(135deg, #8b5cf6, #ec4899)", "-webkit-background-clip": "text", "-webkit-text-fill-color": "transparent"}, "content": "Portfolio"},
                                {"tagName": "div", "style": {"display": "flex", "gap": "28px"},
                                 "components": [
                                     {"tagName": "a", "attributes": {"href": "#work"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".9rem"}, "content": "Work"},
                                     {"tagName": "a", "attributes": {"href": "#about"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".9rem"}, "content": "About"},
                                     {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".9rem"}, "content": "Contact"},
                                 ]},
                            ]
                        },
                        {
                            "tagName": "section",
                            "style": {"padding": "120px 48px 80px", "text-align": "center"},
                            "components": [
                                {"tagName": "p", "style": {"color": "#8b5cf6", "font-size": ".9rem", "font-weight": "600", "letter-spacing": ".15em", "text-transform": "uppercase", "margin": "0 0 16px"}, "content": "Hello, I'm"},
                                {"tagName": "h1", "style": {"font-size": "4rem", "font-weight": "800", "margin": "0 0 20px", "line-height": "1.1", "color": "#fff"}, "content": "Creative<br>Designer"},
                                {"tagName": "p", "style": {"font-size": "1.125rem", "color": "#94a3b8", "max-width": "500px", "margin": "0 auto 40px", "line-height": "1.7"}, "content": "I craft beautiful digital experiences that inspire and engage. Specializing in UI/UX design and web development."},
                                {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center"},
                                 "components": [
                                     {"tagName": "a", "attributes": {"href": "#work"}, "style": {"display": "inline-block", "padding": "14px 32px", "background": "linear-gradient(135deg, #8b5cf6, #ec4899)", "color": "#fff", "border-radius": "50px", "text-decoration": "none", "font-weight": "600"}, "content": "View My Work"},
                                     {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "14px 32px", "background": "transparent", "color": "#fff", "border": "1px solid #334155", "border-radius": "50px", "text-decoration": "none", "font-weight": "600"}, "content": "Hire Me"},
                                 ]}
                            ]
                        },
                        {
                            "tagName": "section",
                            "attributes": {"id": "work"},
                            "style": {"padding": "80px 48px"},
                            "components": [
                                {"tagName": "h2", "style": {"font-size": "2rem", "font-weight": "700", "color": "#fff", "margin": "0 0 48px", "text-align": "center"}, "content": "Selected Work"},
                                {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(2, 1fr)", "gap": "24px", "max-width": "900px", "margin": "0 auto"},
                                 "components": [
                                     *[{"tagName": "div", "style": {"background": bg, "border-radius": "16px", "padding": "48px 32px", "aspect-ratio": "4/3", "display": "flex", "flex-direction": "column", "justify-content": "flex-end"},
                                        "components": [
                                            {"tagName": "span", "style": {"font-size": ".75rem", "color": "rgba(255,255,255,.6)", "text-transform": "uppercase", "letter-spacing": ".1em", "margin-bottom": "8px"}, "content": cat},
                                            {"tagName": "h3", "style": {"font-size": "1.25rem", "font-weight": "700", "color": "#fff", "margin": "0"}, "content": title},
                                        ]} for bg, cat, title in [
                                         ("linear-gradient(135deg, #6366f1, #8b5cf6)", "UI Design", "Mobile Banking App"),
                                         ("linear-gradient(135deg, #ec4899, #f43f5e)", "Branding", "Brand Identity System"),
                                         ("linear-gradient(135deg, #0ea5e9, #6366f1)", "Web Design", "SaaS Dashboard"),
                                         ("linear-gradient(135deg, #10b981, #0ea5e9)", "Development", "E-commerce Platform"),
                                     ]]
                                 ]}
                            ]
                        },
                        {
                            "tagName": "footer",
                            "style": {"padding": "40px 48px", "text-align": "center", "border-top": "1px solid #1e293b"},
                            "components": [
                                {"tagName": "p", "style": {"color": "#475569", "font-size": ".875rem", "margin": "0"}, "content": "© 2025 Creative Portfolio. Crafted with passion."},
                            ]
                        }
                    ]
                }
            }],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 3. Restaurant / Food
    # ─────────────────────────────────────────────
    {
        "name": "Restaurant & Food",
        "slug": "restaurant",
        "category": "food",
        "description": "قالب أنيق للمطاعم والمقاهي مع القائمة وساعات العمل والحجز",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#dc2626",
            "secondary_color": "#991b1b",
            "accent_color": "#f59e0b",
            "background_color": "#fffbf5",
            "text_color": "#1c1917",
            "heading_font": "Georgia",
            "body_font": "Inter",
            "border_radius": "4px",
        },
        "thumbnail_url": "/static/templates/restaurant.png",
        "grapes_data": {
            "pages": [{
                "id": "main",
                "component": {
                    "type": "wrapper",
                    "style": {"font-family": "Inter, sans-serif", "background": "#fffbf5", "color": "#1c1917"},
                    "components": [
                        {
                            "tagName": "nav",
                            "style": {"display": "flex", "align-items": "center", "justify-content": "space-between",
                                      "padding": "20px 48px", "background": "#1c1917"},
                            "components": [
                                {"tagName": "div", "style": {"font-size": "1.75rem", "font-weight": "700", "color": "#f59e0b", "font-family": "Georgia, serif"}, "content": "La Maison"},
                                {"tagName": "div", "style": {"display": "flex", "gap": "28px"},
                                 "components": [
                                     *[{"tagName": "a", "attributes": {"href": f"#{slug}"}, "style": {"color": "#d4d0cb", "text-decoration": "none", "font-size": ".9rem"}, "content": label}
                                       for slug, label in [("menu", "Menu"), ("about", "About"), ("reservation", "Reserve a Table")]]
                                 ]},
                            ]
                        },
                        {
                            "tagName": "section",
                            "style": {"height": "600px", "background": "linear-gradient(rgba(0,0,0,.5), rgba(0,0,0,.4)), url('https://placehold.co/1400x600/1c1917/f59e0b?text=Restaurant') center/cover", "display": "flex", "align-items": "center", "justify-content": "center", "text-align": "center", "color": "#fff"},
                            "components": [
                                {"tagName": "div", "components": [
                                    {"tagName": "p", "style": {"color": "#f59e0b", "font-size": ".9rem", "letter-spacing": ".2em", "text-transform": "uppercase", "margin": "0 0 12px"}, "content": "Fine Dining Experience"},
                                    {"tagName": "h1", "style": {"font-size": "4rem", "font-weight": "700", "margin": "0 0 20px", "font-family": "Georgia, serif"}, "content": "A Taste of Excellence"},
                                    {"tagName": "p", "style": {"font-size": "1.125rem", "color": "#f1f0ee", "margin": "0 0 36px", "max-width": "480px"}, "content": "Experience the finest cuisine crafted from locally sourced ingredients"},
                                    {"tagName": "a", "attributes": {"href": "#reservation"}, "style": {"display": "inline-block", "padding": "14px 36px", "background": "#dc2626", "color": "#fff", "border-radius": "4px", "text-decoration": "none", "font-weight": "600"}, "content": "Reserve Your Table"},
                                ]}
                            ]
                        },
                        {
                            "tagName": "section",
                            "attributes": {"id": "menu"},
                            "style": {"padding": "80px 48px", "background": "#fff"},
                            "components": [
                                {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.5rem", "font-family": "Georgia, serif", "color": "#1c1917", "margin": "0 0 8px"}, "content": "Our Menu"},
                                {"tagName": "p", "style": {"text-align": "center", "color": "#78716c", "margin": "0 auto 48px"}, "content": "Carefully crafted dishes for every occasion"},
                                {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(2, 1fr)", "gap": "0", "max-width": "800px", "margin": "0 auto"},
                                 "components": [
                                     *[{"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "flex-start", "padding": "20px 24px", "border-bottom": "1px solid #f5f0eb"},
                                        "components": [
                                            {"tagName": "div", "components": [
                                                {"tagName": "h4", "style": {"font-size": "1rem", "font-weight": "600", "margin": "0 0 4px", "color": "#1c1917"}, "content": name},
                                                {"tagName": "p", "style": {"font-size": ".8rem", "color": "#78716c", "margin": "0"}, "content": desc},
                                            ]},
                                            {"tagName": "span", "style": {"font-size": "1rem", "font-weight": "700", "color": "#dc2626", "white-space": "nowrap", "margin-left": "16px"}, "content": price},
                                        ]} for name, desc, price in [
                                         ("Grilled Salmon", "Fresh Atlantic salmon with herbs", "$28"),
                                         ("Beef Tenderloin", "Prime cut with truffle sauce", "$42"),
                                         ("Caesar Salad", "Romaine, parmesan, croutons", "$14"),
                                         ("Chocolate Fondant", "Warm with vanilla ice cream", "$12"),
                                     ]]
                                 ]}
                            ]
                        },
                        {
                            "tagName": "footer",
                            "style": {"background": "#1c1917", "color": "#a8a29e", "padding": "40px 48px", "text-align": "center"},
                            "components": [
                                {"tagName": "p", "style": {"font-size": "1.25rem", "color": "#f59e0b", "font-family": "Georgia, serif", "margin": "0 0 8px"}, "content": "La Maison"},
                                {"tagName": "p", "style": {"font-size": ".875rem", "margin": "0"}, "content": "123 Main Street • Open daily 12pm – 11pm • +1 (555) 000-0000"},
                            ]
                        }
                    ]
                }
            }],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 4. Personal Blog
    # ─────────────────────────────────────────────
    {
        "name": "Personal Blog",
        "slug": "personal-blog",
        "category": "blog",
        "description": "قالب مدونة شخصية نظيف وأنيق للكتّاب والمدونين",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#059669",
            "secondary_color": "#047857",
            "accent_color": "#f59e0b",
            "background_color": "#ffffff",
            "text_color": "#111827",
            "heading_font": "Georgia",
            "body_font": "Inter",
            "border_radius": "6px",
        },
        "thumbnail_url": "/static/templates/blog.png",
        "grapes_data": {
            "pages": [{
                "id": "main",
                "component": {
                    "type": "wrapper",
                    "style": {"font-family": "Inter, sans-serif", "background": "#fff", "color": "#111827"},
                    "components": [
                        {
                            "tagName": "header",
                            "style": {"border-bottom": "1px solid #f3f4f6", "padding": "20px 0"},
                            "components": [
                                {"tagName": "div", "style": {"max-width": "760px", "margin": "0 auto", "padding": "0 24px", "display": "flex", "align-items": "center", "justify-content": "space-between"},
                                 "components": [
                                     {"tagName": "div", "components": [
                                         {"tagName": "h1", "style": {"font-size": "1.5rem", "font-weight": "700", "margin": "0", "font-family": "Georgia, serif", "color": "#111827"}, "content": "My Blog"},
                                         {"tagName": "p", "style": {"font-size": ".8rem", "color": "#6b7280", "margin": "2px 0 0"}, "content": "Thoughts, stories and ideas"},
                                     ]},
                                     {"tagName": "nav", "style": {"display": "flex", "gap": "20px"},
                                      "components": [
                                          *[{"tagName": "a", "attributes": {"href": "#"}, "style": {"color": "#6b7280", "text-decoration": "none", "font-size": ".875rem"}, "content": lbl}
                                            for lbl in ["Home", "About", "Archive", "RSS"]]
                                      ]},
                                 ]}
                            ]
                        },
                        {
                            "tagName": "main",
                            "style": {"max-width": "760px", "margin": "0 auto", "padding": "60px 24px"},
                            "components": [
                                {"tagName": "div", "style": {"margin-bottom": "40px", "padding-bottom": "40px", "border-bottom": "1px solid #f3f4f6"},
                                 "components": [
                                     {"tagName": "span", "style": {"font-size": ".75rem", "color": "#059669", "font-weight": "600", "text-transform": "uppercase", "letter-spacing": ".05em"}, "content": "Technology"},
                                     {"tagName": "h2", "style": {"font-size": "2rem", "font-family": "Georgia, serif", "margin": "8px 0 12px", "line-height": "1.3"}, "content": "The Future of Web Development in 2025"},
                                     {"tagName": "p", "style": {"color": "#6b7280", "line-height": "1.7", "margin": "0 0 20px"}, "content": "Web development continues to evolve at a rapid pace. From AI-assisted coding to edge computing, the landscape is changing in ways we couldn't have imagined a few years ago..."},
                                     {"tagName": "div", "style": {"display": "flex", "align-items": "center", "gap": "12px"},
                                      "components": [
                                          {"tagName": "div", "style": {"width": "36px", "height": "36px", "border-radius": "50%", "background": "#059669", "display": "flex", "align-items": "center", "justify-content": "center", "color": "#fff", "font-weight": "700", "font-size": ".875rem"}, "content": "JD"},
                                          {"tagName": "div", "components": [
                                              {"tagName": "p", "style": {"font-size": ".875rem", "font-weight": "600", "margin": "0", "color": "#111827"}, "content": "John Doe"},
                                              {"tagName": "p", "style": {"font-size": ".75rem", "color": "#9ca3af", "margin": "0"}, "content": "April 5, 2025 · 8 min read"},
                                          ]},
                                      ]},
                                 ]},
                                *[{"tagName": "div", "style": {"margin-bottom": "32px", "padding-bottom": "32px", "border-bottom": "1px solid #f3f4f6", "display": "flex", "gap": "20px"},
                                   "components": [
                                       {"tagName": "div", "style": {"flex": "1"},
                                        "components": [
                                            {"tagName": "span", "style": {"font-size": ".7rem", "color": cat_color, "font-weight": "600", "text-transform": "uppercase"}, "content": cat},
                                            {"tagName": "h3", "style": {"font-size": "1.25rem", "font-family": "Georgia, serif", "margin": "6px 0 8px", "line-height": "1.4"}, "content": title},
                                            {"tagName": "p", "style": {"color": "#9ca3af", "font-size": ".8rem", "margin": "0"}, "content": date},
                                        ]},
                                   ]}
                                  for cat, cat_color, title, date in [
                                    ("Design", "#6366f1", "10 Principles of Great UI Design", "March 28, 2025"),
                                    ("Productivity", "#f59e0b", "How I Write 5,000 Words Every Day", "March 15, 2025"),
                                ]]
                            ]
                        },
                        {
                            "tagName": "footer",
                            "style": {"border-top": "1px solid #f3f4f6", "padding": "32px 24px", "text-align": "center"},
                            "components": [
                                {"tagName": "p", "style": {"color": "#9ca3af", "font-size": ".875rem", "margin": "0"}, "content": "© 2025 My Blog · Built with passion"},
                            ]
                        }
                    ]
                }
            }],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 5. SaaS / Startup
    # ─────────────────────────────────────────────
    {
        "name": "SaaS Startup",
        "slug": "saas-startup",
        "category": "saas",
        "description": "قالب عصري لمنتجات SaaS والشركات الناشئة مع pricing وfeatures",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#7c3aed",
            "secondary_color": "#5b21b6",
            "accent_color": "#06b6d4",
            "background_color": "#ffffff",
            "text_color": "#0f172a",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "12px",
        },
        "thumbnail_url": "/static/templates/saas.png",
        "grapes_data": {
            "pages": [{
                "id": "main",
                "component": {
                    "type": "wrapper",
                    "style": {"font-family": "Inter, sans-serif"},
                    "components": [
                        {
                            "tagName": "nav",
                            "style": {"display": "flex", "align-items": "center", "justify-content": "space-between",
                                      "padding": "16px 48px", "background": "#fff", "border-bottom": "1px solid #f1f5f9",
                                      "position": "sticky", "top": "0", "z-index": "50"},
                            "components": [
                                {"tagName": "div", "style": {"font-size": "1.25rem", "font-weight": "800", "color": "#7c3aed"}, "content": "Launchpad"},
                                {"tagName": "div", "style": {"display": "flex", "gap": "32px", "align-items": "center"},
                                 "components": [
                                     *[{"tagName": "a", "attributes": {"href": f"#{s}"}, "style": {"color": "#64748b", "text-decoration": "none", "font-size": ".875rem", "font-weight": "500"}, "content": l}
                                       for s, l in [("features", "Features"), ("pricing", "Pricing"), ("faq", "FAQ")]],
                                     {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "8px 20px", "background": "#7c3aed", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".875rem", "font-weight": "600"}, "content": "Get Started Free"},
                                 ]},
                            ]
                        },
                        {
                            "tagName": "section",
                            "style": {"padding": "100px 48px", "text-align": "center", "background": "radial-gradient(ellipse at top, #ede9fe 0%, #fff 60%)"},
                            "components": [
                                {"tagName": "div", "style": {"display": "inline-flex", "align-items": "center", "gap": "8px", "background": "#ede9fe", "color": "#7c3aed", "padding": "6px 16px", "border-radius": "50px", "font-size": ".8rem", "font-weight": "600", "margin-bottom": "24px"}, "content": "🎉 Now in Public Beta"},
                                {"tagName": "h1", "style": {"font-size": "3.75rem", "font-weight": "800", "line-height": "1.1", "color": "#0f172a", "margin": "0 0 24px", "max-width": "800px", "margin-left": "auto", "margin-right": "auto"}, "content": "Ship Faster.<br>Scale Smarter."},
                                {"tagName": "p", "style": {"font-size": "1.25rem", "color": "#64748b", "max-width": "560px", "margin": "0 auto 40px", "line-height": "1.7"}, "content": "The all-in-one platform that helps teams build, launch, and grow products 10x faster."},
                                {"tagName": "div", "style": {"display": "flex", "gap": "12px", "justify-content": "center", "flex-wrap": "wrap"},
                                 "components": [
                                     {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-flex", "align-items": "center", "gap": "8px", "padding": "14px 32px", "background": "#7c3aed", "color": "#fff", "border-radius": "10px", "text-decoration": "none", "font-weight": "700"}, "content": "Start for Free →"},
                                     {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-flex", "align-items": "center", "gap": "8px", "padding": "14px 32px", "background": "#fff", "color": "#374151", "border": "1px solid #e2e8f0", "border-radius": "10px", "text-decoration": "none", "font-weight": "600"}, "content": "▶ Watch Demo"},
                                 ]},
                            ]
                        },
                        {
                            "tagName": "section",
                            "attributes": {"id": "features"},
                            "style": {"padding": "80px 48px", "background": "#fff"},
                            "components": [
                                {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "margin": "0 0 60px"}, "content": "Everything you need"},
                                {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "32px", "max-width": "1100px", "margin": "0 auto"},
                                 "components": [
                                     *[{"tagName": "div", "style": {"padding": "28px"},
                                        "components": [
                                            {"tagName": "div", "style": {"width": "48px", "height": "48px", "background": "linear-gradient(135deg, #ede9fe, #ddd6fe)", "border-radius": "12px", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "1.5rem", "margin-bottom": "16px"}, "content": icon},
                                            {"tagName": "h3", "style": {"font-size": "1.125rem", "font-weight": "700", "margin": "0 0 8px"}, "content": title},
                                            {"tagName": "p", "style": {"color": "#64748b", "font-size": ".9rem", "line-height": "1.6", "margin": "0"}, "content": desc},
                                        ]}
                                       for icon, title, desc in [
                                         ("⚡", "Lightning Fast", "Deploy globally in under 30 seconds with our edge network."),
                                         ("🔒", "Secure by Default", "SOC 2 compliant with end-to-end encryption."),
                                         ("📊", "Real-time Analytics", "Monitor performance and user behavior in real time."),
                                         ("🔗", "100+ Integrations", "Connect with your favorite tools in one click."),
                                         ("🤖", "AI-Powered", "Built-in AI assistant to help you work smarter."),
                                         ("🌍", "Global Scale", "Serve millions of users with zero infrastructure headaches."),
                                     ]]
                                 ]}
                            ]
                        },
                        {
                            "tagName": "section",
                            "attributes": {"id": "pricing"},
                            "style": {"padding": "80px 48px", "background": "#f8fafc"},
                            "components": [
                                {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "margin": "0 0 8px"}, "content": "Simple Pricing"},
                                {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 56px"}, "content": "No hidden fees. Cancel anytime."},
                                {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "24px", "max-width": "1000px", "margin": "0 auto"},
                                 "components": [
                                     *[{"tagName": "div", "style": {"background": bg, "border-radius": "16px", "padding": "32px", "border": border, "position": "relative"},
                                        "components": [
                                            *([ {"tagName": "div", "style": {"position": "absolute", "top": "-12px", "left": "50%", "transform": "translateX(-50%)", "background": "#7c3aed", "color": "#fff", "padding": "4px 16px", "border-radius": "50px", "font-size": ".75rem", "font-weight": "700"}, "content": "Most Popular"}] if popular else []),
                                            {"tagName": "h3", "style": {"font-size": "1.125rem", "font-weight": "700", "margin": "0 0 8px", "color": title_color}, "content": plan},
                                            {"tagName": "div", "style": {"margin-bottom": "24px"},
                                             "components": [
                                                 {"tagName": "span", "style": {"font-size": "2.5rem", "font-weight": "800", "color": price_color}, "content": price},
                                                 {"tagName": "span", "style": {"color": "#94a3b8", "font-size": ".875rem"}, "content": "/mo"},
                                             ]},
                                            {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "block", "text-align": "center", "padding": "12px", "background": btn_bg, "color": btn_color, "border-radius": "8px", "text-decoration": "none", "font-weight": "600", "font-size": ".875rem"}, "content": "Get Started"},
                                        ]}
                                       for plan, price, bg, border, popular, title_color, price_color, btn_bg, btn_color in [
                                         ("Starter", "$0", "#fff", "1px solid #e2e8f0", False, "#0f172a", "#0f172a", "#f1f5f9", "#374151"),
                                         ("Pro", "$29", "#7c3aed", "none", True, "#fff", "#fff", "rgba(255,255,255,.2)", "#fff"),
                                         ("Enterprise", "$99", "#fff", "1px solid #e2e8f0", False, "#0f172a", "#0f172a", "#f1f5f9", "#374151"),
                                     ]]
                                 ]}
                            ]
                        },
                        {
                            "tagName": "footer",
                            "style": {"background": "#0f172a", "padding": "40px 48px", "text-align": "center"},
                            "components": [
                                {"tagName": "p", "style": {"color": "#475569", "font-size": ".875rem", "margin": "0"}, "content": "© 2025 Launchpad Inc. All rights reserved."},
                            ]
                        }
                    ]
                }
            }],
            "styles": []
        }
    },
    # ─────────────────────────────────────────────
    # 6. Medical / Healthcare Clinic
    # ─────────────────────────────────────────────
    {
        "name": "Medical Clinic",
        "slug": "medical-clinic",
        "category": "health",
        "description": "موقع عيادة طبية احترافي مع حجز مواعيد وعرض الأطباء والخدمات",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#0891b2",
            "secondary_color": "#0e7490",
            "accent_color": "#10b981",
            "background_color": "#f0fdfa",
            "text_color": "#0f172a",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "12px",
        },
        "thumbnail_url": "/static/templates/medical-clinic.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#fff", "box-shadow": "0 1px 4px rgba(0,0,0,.08)", "position": "sticky", "top": "0", "z-index": "100"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "align-items": "center", "gap": "10px"},
                      "components": [
                          {"tagName": "span", "style": {"font-size": "1.6rem"}, "content": "🏥"},
                          {"tagName": "span", "style": {"font-size": "1.25rem", "font-weight": "800", "color": "#0891b2"}, "content": "HealthCare Clinic"},
                      ]},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#services"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "Services"},
                          {"tagName": "a", "attributes": {"href": "#doctors"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "Doctors"},
                          {"tagName": "a", "attributes": {"href": "#appointment"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#0891b2", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "600"}, "content": "Book Appointment"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "90px 48px", "background": "linear-gradient(135deg, #ecfeff 0%, #cffafe 100%)", "display": "flex", "align-items": "center", "gap": "60px"},
                 "components": [
                     {"tagName": "div", "style": {"flex": "1"},
                      "components": [
                          {"tagName": "span", "style": {"display": "inline-block", "background": "#0891b2", "color": "#fff", "padding": "6px 16px", "border-radius": "20px", "font-size": ".8rem", "font-weight": "600", "margin-bottom": "20px"}, "content": "Trusted Healthcare"},
                          {"tagName": "h1", "style": {"font-size": "3rem", "font-weight": "800", "color": "#0f172a", "margin": "0 0 20px", "line-height": "1.2"}, "content": "Your Health Is Our Priority"},
                          {"tagName": "p", "style": {"font-size": "1.1rem", "color": "#475569", "line-height": "1.7", "margin": "0 0 36px", "max-width": "480px"}, "content": "Expert medical care with state-of-the-art facilities. Our team of specialists is dedicated to your wellbeing."},
                          {"tagName": "div", "style": {"display": "flex", "gap": "16px"},
                           "components": [
                               {"tagName": "a", "attributes": {"href": "#appointment"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#0891b2", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "Book Now"},
                               {"tagName": "a", "attributes": {"href": "#services"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "2px solid #0891b2", "color": "#0891b2", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "Our Services"},
                           ]},
                      ]},
                     {"tagName": "div", "style": {"flex": "1", "display": "grid", "grid-template-columns": "1fr 1fr", "gap": "16px"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#fff", "border-radius": "12px", "padding": "24px", "box-shadow": "0 2px 8px rgba(8,145,178,.1)", "text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2rem", "margin-bottom": "8px"}, "content": ic},
                                 {"tagName": "div", "style": {"font-weight": "700", "color": "#0f172a", "font-size": ".95rem"}, "content": lb},
                             ]} for ic, lb in [("❤️", "Cardiology"), ("🧠", "Neurology"), ("🦷", "Dentistry"), ("👁️", "Ophthalmology")]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "services"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 12px"}, "content": "Medical Services"},
                     {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 52px", "max-width": "500px"}, "content": "Comprehensive healthcare services for you and your family"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(4, 1fr)", "gap": "24px", "max-width": "1100px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "28px 20px", "border": "1px solid #e0f2fe", "border-radius": "12px", "text-align": "center", "background": "#f0fdfa"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2.2rem", "margin-bottom": "12px"}, "content": ic},
                                 {"tagName": "h3", "style": {"font-size": "1rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 8px"}, "content": svc},
                                 {"tagName": "p", "style": {"font-size": ".85rem", "color": "#64748b", "margin": "0", "line-height": "1.5"}, "content": desc},
                             ]} for ic, svc, desc in [
                              ("🔬", "Lab Tests", "Fast & accurate diagnostic testing"),
                              ("💊", "Pharmacy", "On-site pharmacy with 24/7 service"),
                              ("🩺", "Check-ups", "Complete annual health checkups"),
                              ("🚑", "Emergency", "24/7 emergency care services"),
                              ("🧬", "Genetics", "DNA and genetic counseling"),
                              ("🏃", "Physiotherapy", "Rehabilitation & recovery"),
                              ("👶", "Pediatrics", "Specialized child healthcare"),
                              ("🧘", "Mental Health", "Counseling & psychiatric care"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "doctors"}, "style": {"padding": "80px 48px", "background": "#f0fdfa"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 48px"}, "content": "Our Specialist Doctors"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "900px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#fff", "border-radius": "16px", "padding": "32px 24px", "text-align": "center", "box-shadow": "0 4px 16px rgba(8,145,178,.08)"},
                             "components": [
                                 {"tagName": "div", "style": {"width": "80px", "height": "80px", "border-radius": "50%", "background": "linear-gradient(135deg, #0891b2, #06b6d4)", "margin": "0 auto 16px", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "2rem"}, "content": av},
                                 {"tagName": "h3", "style": {"font-size": "1.1rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 4px"}, "content": nm},
                                 {"tagName": "p", "style": {"color": "#0891b2", "font-size": ".85rem", "font-weight": "600", "margin": "0"}, "content": sp},
                             ]} for av, nm, sp in [
                              ("👨‍⚕️", "Dr. Ahmed Hassan", "Cardiologist"),
                              ("👩‍⚕️", "Dr. Sara Ali", "Neurologist"),
                              ("👨‍⚕️", "Dr. Khalid Omar", "Orthopedist"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "appointment"}, "style": {"padding": "80px 48px", "background": "#0891b2", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "700", "color": "#fff", "margin": "0 0 12px"}, "content": "Book an Appointment"},
                     {"tagName": "p", "style": {"color": "#cffafe", "margin": "0 0 36px", "font-size": "1.1rem"}, "content": "Call us or fill the form — we'll confirm within 2 hours"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "tel:+966500000000"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#fff", "color": "#0891b2", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "📞 Call Now"},
                          {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "2px solid #fff", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "Online Booking"},
                      ]},
                 ]},
                {"tagName": "footer", "style": {"background": "#0f172a", "color": "#94a3b8", "padding": "32px 48px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 HealthCare Clinic. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 7. Real Estate Agency
    # ─────────────────────────────────────────────
    {
        "name": "Real Estate Agency",
        "slug": "real-estate",
        "category": "realestate",
        "description": "موقع وكالة عقارية مع عرض العقارات والبحث والتواصل مع الوكلاء",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#059669",
            "secondary_color": "#047857",
            "accent_color": "#f59e0b",
            "background_color": "#f8fafc",
            "text_color": "#0f172a",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "8px",
        },
        "thumbnail_url": "/static/templates/real-estate.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#fff", "box-shadow": "0 1px 4px rgba(0,0,0,.08)", "position": "sticky", "top": "0", "z-index": "100"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.4rem", "font-weight": "800", "color": "#059669"}, "content": "🏡 HomeFinder"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#listings"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Listings"},
                          {"tagName": "a", "attributes": {"href": "#agents"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Agents"},
                          {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#059669", "color": "#fff", "border-radius": "6px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "600"}, "content": "List Property"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "100px 48px", "background": "linear-gradient(rgba(0,0,0,.5),rgba(0,0,0,.5)), url('https://images.unsplash.com/photo-1560518883-ce09059eeffa?w=1600') center/cover", "text-align": "center", "color": "#fff"},
                 "components": [
                     {"tagName": "h1", "style": {"font-size": "3.5rem", "font-weight": "800", "margin": "0 0 16px", "line-height": "1.15"}, "content": "Find Your Dream Home"},
                     {"tagName": "p", "style": {"font-size": "1.2rem", "margin": "0 auto 40px", "max-width": "560px", "opacity": ".9"}, "content": "Thousands of properties — houses, apartments, villas — in the best locations."},
                     {"tagName": "div", "style": {"display": "flex", "background": "#fff", "border-radius": "10px", "overflow": "hidden", "max-width": "600px", "margin": "0 auto", "box-shadow": "0 8px 32px rgba(0,0,0,.2)"},
                      "components": [
                          {"tagName": "input", "attributes": {"type": "text", "placeholder": "🔍  City, neighborhood or address..."}, "style": {"flex": "1", "padding": "16px 20px", "border": "none", "font-size": ".95rem", "color": "#0f172a", "outline": "none"}},
                          {"tagName": "button", "style": {"padding": "16px 28px", "background": "#059669", "color": "#fff", "border": "none", "font-weight": "700", "font-size": ".95rem", "cursor": "pointer"}, "content": "Search"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "24px 48px", "background": "#f1f5f9"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "gap": "40px", "justify-content": "center", "max-width": "800px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "1.75rem", "font-weight": "800", "color": "#059669"}, "content": num},
                                 {"tagName": "div", "style": {"font-size": ".85rem", "color": "#64748b"}, "content": lbl},
                             ]} for num, lbl in [("1,200+", "Properties Listed"), ("500+", "Happy Clients"), ("50+", "Expert Agents"), ("15+", "Years Experience")]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "listings"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 12px"}, "content": "Featured Properties"},
                     {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 52px"}, "content": "Handpicked properties just for you"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "1100px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"border-radius": "14px", "overflow": "hidden", "box-shadow": "0 4px 16px rgba(0,0,0,.08)", "background": "#fff"},
                             "components": [
                                 {"tagName": "div", "style": {"background": f"linear-gradient(135deg, {c1}, {c2})", "height": "200px", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "4rem"}, "content": ic},
                                 {"tagName": "div", "style": {"padding": "20px"},
                                  "components": [
                                      {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center", "margin-bottom": "8px"},
                                       "components": [
                                           {"tagName": "h3", "style": {"font-size": "1.1rem", "font-weight": "700", "color": "#0f172a", "margin": "0"}, "content": nm},
                                           {"tagName": "span", "style": {"font-size": "1.1rem", "font-weight": "800", "color": "#059669"}, "content": pr},
                                       ]},
                                      {"tagName": "p", "style": {"color": "#64748b", "font-size": ".85rem", "margin": "0 0 12px"}, "content": loc},
                                      {"tagName": "div", "style": {"display": "flex", "gap": "16px", "font-size": ".8rem", "color": "#94a3b8"},
                                       "components": [
                                           {"tagName": "span", "content": f"🛏 {bd} Beds"},
                                           {"tagName": "span", "content": f"🚿 {ba} Bath"},
                                           {"tagName": "span", "content": sz},
                                       ]},
                                  ]},
                             ]} for ic, nm, pr, loc, bd, ba, sz, c1, c2 in [
                              ("🏠", "Modern Villa", "$850,000", "📍 Beverly Hills, CA", "4", "3", "3,200 sqft", "#ecfdf5", "#d1fae5"),
                              ("🏢", "City Apartment", "$320,000", "📍 Downtown, NY", "2", "2", "1,100 sqft", "#eff6ff", "#dbeafe"),
                              ("🌴", "Beach House", "$1,200,000", "📍 Malibu, CA", "5", "4", "4,500 sqft", "#fff7ed", "#fed7aa"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "contact"}, "style": {"padding": "80px 48px", "background": "#059669", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "700", "color": "#fff", "margin": "0 0 12px"}, "content": "Ready to Find Your Home?"},
                     {"tagName": "p", "style": {"color": "#d1fae5", "font-size": "1.1rem", "margin": "0 0 36px"}, "content": "Talk to our expert agents — free consultation"},
                     {"tagName": "a", "attributes": {"href": "tel:+1-800-555-0123"}, "style": {"display": "inline-block", "padding": "14px 40px", "background": "#fff", "color": "#059669", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1.1rem"}, "content": "📞 (800) 555-0123"},
                 ]},
                {"tagName": "footer", "style": {"background": "#0f172a", "color": "#94a3b8", "padding": "32px 48px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 HomeFinder Real Estate. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 8. Online Education / Course Platform
    # ─────────────────────────────────────────────
    {
        "name": "Online Education",
        "slug": "online-education",
        "category": "education",
        "description": "منصة تعليمية لعرض الكورسات والمحاضرات مع نماذج التسجيل",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#7c3aed",
            "secondary_color": "#6d28d9",
            "accent_color": "#f59e0b",
            "background_color": "#faf5ff",
            "text_color": "#1e1b4b",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "10px",
        },
        "thumbnail_url": "/static/templates/education.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#fff", "box-shadow": "0 1px 4px rgba(0,0,0,.08)", "position": "sticky", "top": "0", "z-index": "100"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.4rem", "font-weight": "800", "color": "#7c3aed"}, "content": "🎓 LearnSpace"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#courses"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Courses"},
                          {"tagName": "a", "attributes": {"href": "#instructors"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Instructors"},
                          {"tagName": "a", "attributes": {"href": "#pricing"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#7c3aed", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "600"}, "content": "Get Started"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "90px 48px", "background": "linear-gradient(135deg, #faf5ff 0%, #ede9fe 100%)", "display": "flex", "align-items": "center", "gap": "60px"},
                 "components": [
                     {"tagName": "div", "style": {"flex": "1"},
                      "components": [
                          {"tagName": "span", "style": {"display": "inline-block", "background": "#ede9fe", "color": "#7c3aed", "padding": "6px 16px", "border-radius": "20px", "font-size": ".8rem", "font-weight": "600", "margin-bottom": "20px"}, "content": "✨ 500+ Online Courses"},
                          {"tagName": "h1", "style": {"font-size": "3rem", "font-weight": "800", "color": "#1e1b4b", "margin": "0 0 20px", "line-height": "1.2"}, "content": "Learn Without Limits"},
                          {"tagName": "p", "style": {"font-size": "1.1rem", "color": "#64748b", "line-height": "1.7", "margin": "0 0 36px", "max-width": "480px"}, "content": "Master new skills with expert-led courses. Learn at your own pace, anywhere, anytime."},
                          {"tagName": "div", "style": {"display": "flex", "gap": "16px"},
                           "components": [
                               {"tagName": "a", "attributes": {"href": "#courses"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#7c3aed", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "Explore Courses"},
                               {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "2px solid #7c3aed", "color": "#7c3aed", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "▶ Watch Demo"},
                           ]},
                      ]},
                     {"tagName": "div", "style": {"flex": "1", "display": "grid", "grid-template-columns": "1fr 1fr", "gap": "16px"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#fff", "border-radius": "12px", "padding": "20px", "box-shadow": "0 4px 16px rgba(124,58,237,.1)", "text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2rem", "margin-bottom": "8px"}, "content": ic},
                                 {"tagName": "div", "style": {"font-weight": "700", "color": "#7c3aed", "font-size": "1.4rem"}, "content": num},
                                 {"tagName": "div", "style": {"color": "#64748b", "font-size": ".8rem"}, "content": lbl},
                             ]} for ic, num, lbl in [("📚", "500+", "Courses"), ("👨‍🎓", "50K+", "Students"), ("🏆", "200+", "Instructors"), ("⭐", "4.9", "Avg Rating")]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "courses"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#1e1b4b", "margin": "0 0 12px"}, "content": "Popular Courses"},
                     {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 52px"}, "content": "Start learning with our most enrolled courses"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "1100px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"border-radius": "14px", "overflow": "hidden", "box-shadow": "0 4px 16px rgba(0,0,0,.08)", "background": "#fff"},
                             "components": [
                                 {"tagName": "div", "style": {"height": "160px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "3.5rem"}, "content": ic},
                                 {"tagName": "div", "style": {"padding": "20px"},
                                  "components": [
                                      {"tagName": "span", "style": {"background": "#ede9fe", "color": "#7c3aed", "padding": "3px 10px", "border-radius": "12px", "font-size": ".75rem", "font-weight": "600"}, "content": cat},
                                      {"tagName": "h3", "style": {"font-size": "1.05rem", "font-weight": "700", "color": "#1e1b4b", "margin": "12px 0 8px"}, "content": nm},
                                      {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center"},
                                       "components": [
                                           {"tagName": "span", "style": {"color": "#64748b", "font-size": ".85rem"}, "content": f"⏱ {dur}"},
                                           {"tagName": "span", "style": {"font-weight": "800", "color": "#7c3aed", "font-size": "1.1rem"}, "content": pr},
                                       ]},
                                  ]},
                             ]} for ic, nm, cat, dur, pr, c1, c2 in [
                              ("💻", "Full-Stack Web Dev", "Development", "48 hours", "$49", "#ede9fe", "#ddd6fe"),
                              ("🤖", "AI & Machine Learning", "Technology", "36 hours", "$59", "#ecfdf5", "#d1fae5"),
                              ("📊", "Data Science Bootcamp", "Data", "52 hours", "$69", "#fff7ed", "#fed7aa"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "pricing"}, "style": {"padding": "80px 48px", "background": "#faf5ff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#1e1b4b", "margin": "0 0 48px"}, "content": "Simple Pricing"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "24px", "max-width": "900px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "36px 28px", "background": bg, "border-radius": "16px", "text-align": "center", "border": brd, "box-shadow": sh},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "1rem", "font-weight": "700", "color": tc, "margin-bottom": "8px", "text-transform": "uppercase", "letter-spacing": ".08em"}, "content": plan},
                                 {"tagName": "div", "style": {"font-size": "3rem", "font-weight": "800", "color": tc, "margin": "16px 0"}, "content": price},
                                 {"tagName": "p", "style": {"color": sc, "font-size": ".9rem", "margin": "0 0 28px"}, "content": feat},
                                 {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "block", "padding": "12px", "background": btn_bg, "color": btn_tc, "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "Get Started"},
                             ]} for plan, price, feat, bg, brd, sh, tc, sc, btn_bg, btn_tc in [
                              ("Starter", "$0/mo", "5 courses · Community access", "#fff", "1px solid #e2e8f0", "none", "#1e1b4b", "#64748b", "#ede9fe", "#7c3aed"),
                              ("Pro", "$29/mo", "Unlimited courses · Certificate", "#7c3aed", "none", "0 8px 32px rgba(124,58,237,.3)", "#fff", "#ddd6fe", "#fff", "#7c3aed"),
                              ("Team", "$99/mo", "10 seats · Admin dashboard", "#fff", "1px solid #e2e8f0", "none", "#1e1b4b", "#64748b", "#ede9fe", "#7c3aed"),
                          ]],
                      ]},
                 ]},
                {"tagName": "footer", "style": {"background": "#1e1b4b", "color": "#94a3b8", "padding": "32px 48px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 LearnSpace. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 9. Gym & Fitness Center
    # ─────────────────────────────────────────────
    {
        "name": "Gym & Fitness",
        "slug": "gym-fitness",
        "category": "fitness",
        "description": "موقع نادي رياضي مع الخطط والجداول وعرض المدربين",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#dc2626",
            "secondary_color": "#b91c1c",
            "accent_color": "#f59e0b",
            "background_color": "#0f172a",
            "text_color": "#f8fafc",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "6px",
        },
        "thumbnail_url": "/static/templates/gym.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#0f172a", "border-bottom": "1px solid #1e293b"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.5rem", "font-weight": "900", "color": "#dc2626", "letter-spacing": "-.02em"}, "content": "⚡ IRONFIT"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#programs"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "Programs"},
                          {"tagName": "a", "attributes": {"href": "#trainers"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".9rem", "font-weight": "500"}, "content": "Trainers"},
                          {"tagName": "a", "attributes": {"href": "#join"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#dc2626", "color": "#fff", "border-radius": "6px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "700"}, "content": "JOIN NOW"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "110px 48px", "background": "linear-gradient(rgba(15,23,42,.7),rgba(15,23,42,.9)), url('https://images.unsplash.com/photo-1534438327276-14e5300c3a48?w=1600') center/cover", "text-align": "center"},
                 "components": [
                     {"tagName": "h1", "style": {"font-size": "4rem", "font-weight": "900", "color": "#fff", "margin": "0 0 20px", "text-transform": "uppercase", "letter-spacing": "-.02em", "line-height": "1.1"}, "content": "Unleash Your Potential"},
                     {"tagName": "p", "style": {"font-size": "1.2rem", "color": "#94a3b8", "margin": "0 auto 40px", "max-width": "550px"}, "content": "State-of-the-art equipment, expert trainers, and a community that pushes you to be your best."},
                     {"tagName": "a", "attributes": {"href": "#join"}, "style": {"display": "inline-block", "padding": "16px 48px", "background": "#dc2626", "color": "#fff", "border-radius": "6px", "text-decoration": "none", "font-weight": "800", "font-size": "1.1rem", "text-transform": "uppercase", "letter-spacing": ".05em"}, "content": "Start Free Trial"},
                 ]},
                {"tagName": "section", "style": {"padding": "40px 48px", "background": "#dc2626"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "gap": "48px", "justify-content": "center", "max-width": "900px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2rem", "font-weight": "900", "color": "#fff"}, "content": num},
                                 {"tagName": "div", "style": {"font-size": ".85rem", "color": "#fca5a5", "text-transform": "uppercase", "letter-spacing": ".08em"}, "content": lbl},
                             ]} for num, lbl in [("5K+", "Members"), ("50+", "Equipment"), ("20+", "Classes/Week"), ("15+", "Expert Trainers")]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "programs"}, "style": {"padding": "80px 48px", "background": "#0f172a"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "800", "color": "#fff", "margin": "0 0 48px", "text-transform": "uppercase"}, "content": "Training Programs"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "24px", "max-width": "1000px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#1e293b", "border-radius": "12px", "overflow": "hidden"},
                             "components": [
                                 {"tagName": "div", "style": {"height": "140px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "3.5rem"}, "content": ic},
                                 {"tagName": "div", "style": {"padding": "20px"},
                                  "components": [
                                      {"tagName": "h3", "style": {"font-size": "1.1rem", "font-weight": "800", "color": "#fff", "margin": "0 0 8px", "text-transform": "uppercase"}, "content": nm},
                                      {"tagName": "p", "style": {"color": "#64748b", "font-size": ".85rem", "margin": "0 0 16px", "line-height": "1.5"}, "content": desc},
                                      {"tagName": "span", "style": {"background": "#dc2626", "color": "#fff", "padding": "4px 12px", "border-radius": "4px", "font-size": ".78rem", "font-weight": "700"}, "content": lvl},
                                  ]},
                             ]} for ic, nm, desc, lvl, c1, c2 in [
                              ("🏋️", "Strength Training", "Build muscle and increase strength with our powerlifting program.", "Intermediate", "#1e293b", "#dc2626"),
                              ("🔥", "HIIT Cardio", "High-intensity interval training for maximum calorie burn.", "All Levels", "#1e293b", "#f59e0b"),
                              ("🥊", "Boxing", "Learn technique, build endurance, and boost confidence.", "Beginner", "#1e293b", "#7c3aed"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "join"}, "style": {"padding": "80px 48px", "background": "#1e293b", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.5rem", "font-weight": "900", "color": "#fff", "margin": "0 0 12px", "text-transform": "uppercase"}, "content": "Ready to Transform?"},
                     {"tagName": "p", "style": {"color": "#64748b", "margin": "0 0 36px", "font-size": "1.1rem"}, "content": "First month FREE — no contracts, cancel anytime."},
                     {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "16px 48px", "background": "#dc2626", "color": "#fff", "border-radius": "6px", "text-decoration": "none", "font-weight": "800", "font-size": "1.1rem", "text-transform": "uppercase"}, "content": "Claim Free Month"},
                 ]},
                {"tagName": "footer", "style": {"background": "#020617", "color": "#475569", "padding": "32px 48px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 IRONFIT Gym. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 10. Travel Agency
    # ─────────────────────────────────────────────
    {
        "name": "Travel Agency",
        "slug": "travel-agency",
        "category": "travel",
        "description": "وكالة سفر وسياحة مع عرض الباقات والوجهات والحجز",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#0284c7",
            "secondary_color": "#0369a1",
            "accent_color": "#f59e0b",
            "background_color": "#f0f9ff",
            "text_color": "#0c4a6e",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "12px",
        },
        "thumbnail_url": "/static/templates/travel.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "rgba(255,255,255,.95)", "backdrop-filter": "blur(8px)", "position": "sticky", "top": "0", "z-index": "100", "box-shadow": "0 1px 4px rgba(0,0,0,.08)"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.4rem", "font-weight": "800", "color": "#0284c7"}, "content": "✈️ WanderWorld"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#destinations"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Destinations"},
                          {"tagName": "a", "attributes": {"href": "#packages"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Packages"},
                          {"tagName": "a", "attributes": {"href": "#book"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#0284c7", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "600"}, "content": "Book Now"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "120px 48px", "background": "linear-gradient(rgba(0,0,0,.4),rgba(0,0,0,.5)), url('https://images.unsplash.com/photo-1507525428034-b723cf961d3e?w=1600') center/cover", "text-align": "center", "color": "#fff"},
                 "components": [
                     {"tagName": "h1", "style": {"font-size": "3.5rem", "font-weight": "800", "margin": "0 0 16px", "line-height": "1.15", "text-shadow": "0 2px 8px rgba(0,0,0,.3)"}, "content": "Explore the World"},
                     {"tagName": "p", "style": {"font-size": "1.25rem", "margin": "0 auto 48px", "max-width": "550px", "opacity": ".9"}, "content": "Unforgettable journeys crafted just for you. From tropical beaches to mountain adventures."},
                     {"tagName": "div", "style": {"display": "flex", "background": "#fff", "border-radius": "12px", "overflow": "hidden", "max-width": "700px", "margin": "0 auto", "box-shadow": "0 8px 32px rgba(0,0,0,.2)"},
                      "components": [
                          {"tagName": "input", "attributes": {"type": "text", "placeholder": "🌍  Where do you want to go?"}, "style": {"flex": "1", "padding": "18px 20px", "border": "none", "font-size": ".95rem", "color": "#0f172a", "outline": "none"}},
                          {"tagName": "button", "style": {"padding": "18px 32px", "background": "#0284c7", "color": "#fff", "border": "none", "font-weight": "700", "font-size": ".95rem", "cursor": "pointer"}, "content": "Search"},
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "destinations"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#0c4a6e", "margin": "0 0 12px"}, "content": "Popular Destinations"},
                     {"tagName": "p", "style": {"text-align": "center", "color": "#64748b", "margin": "0 auto 52px"}, "content": "Handpicked destinations for every type of traveler"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(4, 1fr)", "gap": "20px", "max-width": "1100px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"border-radius": "14px", "overflow": "hidden", "box-shadow": "0 4px 16px rgba(0,0,0,.1)", "position": "relative"},
                             "components": [
                                 {"tagName": "div", "style": {"height": "200px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "4rem"}, "content": ic},
                                 {"tagName": "div", "style": {"padding": "16px"},
                                  "components": [
                                      {"tagName": "h3", "style": {"font-size": "1rem", "font-weight": "700", "color": "#0c4a6e", "margin": "0 0 4px"}, "content": nm},
                                      {"tagName": "p", "style": {"color": "#64748b", "font-size": ".8rem", "margin": "0"}, "content": f"From {pr}"},
                                  ]},
                             ]} for ic, nm, pr, c1, c2 in [
                              ("🌴", "Bali, Indonesia", "$899", "#ecfdf5", "#d1fae5"),
                              ("🗼", "Paris, France", "$1,299", "#eff6ff", "#dbeafe"),
                              ("🏔️", "Swiss Alps", "$1,599", "#f0fdf4", "#dcfce7"),
                              ("🌊", "Maldives", "$2,199", "#f0f9ff", "#e0f2fe"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "packages"}, "style": {"padding": "80px 48px", "background": "#f0f9ff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#0c4a6e", "margin": "0 0 48px"}, "content": "Travel Packages"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "1000px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#fff", "border-radius": "16px", "overflow": "hidden", "box-shadow": "0 4px 20px rgba(2,132,199,.1)"},
                             "components": [
                                 {"tagName": "div", "style": {"height": "160px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "3.5rem"}, "content": ic},
                                 {"tagName": "div", "style": {"padding": "24px"},
                                  "components": [
                                      {"tagName": "h3", "style": {"font-size": "1.15rem", "font-weight": "700", "color": "#0c4a6e", "margin": "0 0 8px"}, "content": nm},
                                      {"tagName": "p", "style": {"color": "#64748b", "font-size": ".85rem", "margin": "0 0 16px", "line-height": "1.6"}, "content": desc},
                                      {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center"},
                                       "components": [
                                           {"tagName": "span", "style": {"font-size": "1.25rem", "font-weight": "800", "color": "#0284c7"}, "content": pr},
                                           {"tagName": "a", "attributes": {"href": "#book"}, "style": {"padding": "8px 20px", "background": "#0284c7", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "600", "font-size": ".85rem"}, "content": "Book"},
                                       ]},
                                  ]},
                             ]} for ic, nm, desc, pr, c1, c2 in [
                              ("🌞", "Beach Paradise", "7 nights in Maldives — all inclusive, snorkeling & spa.", "$2,199", "#f0f9ff", "#bae6fd"),
                              ("🏛️", "Cultural Europe", "10 days across Paris, Rome & Barcelona with guided tours.", "$1,899", "#faf5ff", "#ede9fe"),
                              ("🧗", "Adventure Trek", "Nepal Himalaya 14-day guided trek with all gear included.", "$3,499", "#f0fdf4", "#dcfce7"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "book"}, "style": {"padding": "80px 48px", "background": "#0284c7", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "700", "color": "#fff", "margin": "0 0 12px"}, "content": "Start Your Journey Today"},
                     {"tagName": "p", "style": {"color": "#bae6fd", "font-size": "1.1rem", "margin": "0 0 36px"}, "content": "Talk to our travel experts — free trip planning"},
                     {"tagName": "a", "attributes": {"href": "tel:+1-800-WANDER"}, "style": {"display": "inline-block", "padding": "14px 40px", "background": "#fff", "color": "#0284c7", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1.1rem"}, "content": "📞 Call Our Travel Experts"},
                 ]},
                {"tagName": "footer", "style": {"background": "#0c4a6e", "color": "#7dd3fc", "padding": "32px 48px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".875rem"}, "content": "© 2025 WanderWorld Travel Agency. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 11. Law Firm
    # ─────────────────────────────────────────────
    {
        "name": "Law Firm",
        "slug": "law-firm",
        "category": "legal",
        "description": "موقع مكتب محاماة احترافي مع عرض الخدمات القانونية والمحامين",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#1e3a5f",
            "secondary_color": "#152d4a",
            "accent_color": "#c8a96e",
            "background_color": "#f8f7f4",
            "text_color": "#1a1a1a",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "4px",
        },
        "thumbnail_url": "/static/templates/law-firm.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "20px 60px", "background": "#1e3a5f"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "align-items": "center", "gap": "12px"},
                      "components": [
                          {"tagName": "span", "style": {"font-size": "1.5rem"}, "content": "⚖️"},
                          {"tagName": "div",
                           "components": [
                               {"tagName": "div", "style": {"font-size": "1.1rem", "font-weight": "700", "color": "#fff"}, "content": "Hassan & Partners"},
                               {"tagName": "div", "style": {"font-size": ".7rem", "color": "#c8a96e", "letter-spacing": ".1em", "text-transform": "uppercase"}, "content": "Attorneys at Law"},
                           ]},
                      ]},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#practice"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".85rem", "font-weight": "500"}, "content": "Practice Areas"},
                          {"tagName": "a", "attributes": {"href": "#attorneys"}, "style": {"color": "#94a3b8", "text-decoration": "none", "font-size": ".85rem", "font-weight": "500"}, "content": "Attorneys"},
                          {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "9px 24px", "background": "#c8a96e", "color": "#fff", "text-decoration": "none", "font-size": ".85rem", "font-weight": "700", "border-radius": "2px"}, "content": "Free Consultation"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "110px 60px", "background": "linear-gradient(rgba(30,58,95,.88),rgba(30,58,95,.95)), url('https://images.unsplash.com/photo-1589829545856-d10d557cf95f?w=1600') center/cover"},
                 "components": [
                     {"tagName": "div", "style": {"max-width": "700px"},
                      "components": [
                          {"tagName": "div", "style": {"width": "48px", "height": "3px", "background": "#c8a96e", "margin-bottom": "28px"}, "content": ""},
                          {"tagName": "h1", "style": {"font-size": "3rem", "font-weight": "700", "color": "#fff", "margin": "0 0 24px", "line-height": "1.2"}, "content": "Justice. Excellence. Integrity."},
                          {"tagName": "p", "style": {"font-size": "1.1rem", "color": "#94a3b8", "line-height": "1.8", "margin": "0 0 40px", "max-width": "560px"}, "content": "With over 25 years of experience, we provide expert legal counsel across corporate law, litigation, and family matters."},
                          {"tagName": "div", "style": {"display": "flex", "gap": "16px"},
                           "components": [
                               {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#c8a96e", "color": "#fff", "text-decoration": "none", "font-weight": "700"}, "content": "Free Consultation"},
                               {"tagName": "a", "attributes": {"href": "#practice"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "1px solid #94a3b8", "color": "#fff", "text-decoration": "none", "font-weight": "600"}, "content": "Our Services"},
                           ]},
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "practice"}, "style": {"padding": "80px 60px", "background": "#f8f7f4"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2rem", "font-weight": "700", "color": "#1e3a5f", "margin": "0 0 8px"}, "content": "Practice Areas"},
                     {"tagName": "div", "style": {"width": "40px", "height": "3px", "background": "#c8a96e", "margin": "0 0 48px"}, "content": ""},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "24px", "max-width": "1000px"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "28px", "background": "#fff", "border-left": "3px solid #c8a96e", "box-shadow": "0 2px 8px rgba(0,0,0,.06)"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "1.6rem", "margin-bottom": "12px"}, "content": ic},
                                 {"tagName": "h3", "style": {"font-size": "1rem", "font-weight": "700", "color": "#1e3a5f", "margin": "0 0 8px"}, "content": nm},
                                 {"tagName": "p", "style": {"color": "#64748b", "font-size": ".85rem", "margin": "0", "line-height": "1.6"}, "content": desc},
                             ]} for ic, nm, desc in [
                              ("🏢", "Corporate Law", "Business formation, contracts, M&A, and corporate governance."),
                              ("⚖️", "Litigation", "Expert courtroom representation for civil and commercial disputes."),
                              ("👨‍👩‍👧", "Family Law", "Divorce, custody, alimony, and adoption matters."),
                              ("🏠", "Real Estate", "Property transactions, disputes, and landlord-tenant law."),
                              ("💼", "Employment Law", "Wrongful termination, discrimination, and labor disputes."),
                              ("🌐", "Immigration", "Visas, residency, citizenship, and deportation defense."),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "contact"}, "style": {"padding": "80px 60px", "background": "#1e3a5f", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2rem", "font-weight": "700", "color": "#fff", "margin": "0 0 12px"}, "content": "Schedule a Free Consultation"},
                     {"tagName": "p", "style": {"color": "#94a3b8", "font-size": "1rem", "margin": "0 0 36px"}, "content": "Available Mon–Sat, 9 AM – 6 PM. Confidential & no obligation."},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "tel:+1-800-555-LAW"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#c8a96e", "color": "#fff", "text-decoration": "none", "font-weight": "700"}, "content": "📞 Call Us"},
                          {"tagName": "a", "attributes": {"href": "mailto:info@hassanlaw.com"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "1px solid #94a3b8", "color": "#fff", "text-decoration": "none", "font-weight": "600"}, "content": "✉ Email Us"},
                      ]},
                 ]},
                {"tagName": "footer", "style": {"background": "#0f1f33", "color": "#64748b", "padding": "28px 60px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".8rem"}, "content": "© 2025 Hassan & Partners Law Firm. All rights reserved. This website is for informational purposes only."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 12. Photography Studio
    # ─────────────────────────────────────────────
    {
        "name": "Photography Studio",
        "slug": "photography-studio",
        "category": "portfolio",
        "description": "موقع استوديو تصوير احترافي مع معرض الأعمال وحجز الجلسات",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#18181b",
            "secondary_color": "#3f3f46",
            "accent_color": "#f4f0eb",
            "background_color": "#18181b",
            "text_color": "#fafafa",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "4px",
        },
        "thumbnail_url": "/static/templates/photography.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "20px 48px", "background": "#18181b", "border-bottom": "1px solid #27272a"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.25rem", "font-weight": "700", "color": "#fafafa", "letter-spacing": "-.01em"}, "content": "📸 LENS & LIGHT"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#gallery"}, "style": {"color": "#a1a1aa", "text-decoration": "none", "font-size": ".9rem"}, "content": "Gallery"},
                          {"tagName": "a", "attributes": {"href": "#services"}, "style": {"color": "#a1a1aa", "text-decoration": "none", "font-size": ".9rem"}, "content": "Services"},
                          {"tagName": "a", "attributes": {"href": "#book"}, "style": {"display": "inline-block", "padding": "8px 20px", "border": "1px solid #fafafa", "color": "#fafafa", "text-decoration": "none", "font-size": ".85rem", "font-weight": "600"}, "content": "Book Session"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "120px 48px", "background": "#18181b", "text-align": "center"},
                 "components": [
                     {"tagName": "p", "style": {"font-size": ".8rem", "letter-spacing": ".2em", "color": "#71717a", "text-transform": "uppercase", "margin": "0 0 20px"}, "content": "Professional Photography"},
                     {"tagName": "h1", "style": {"font-size": "4rem", "font-weight": "300", "color": "#fafafa", "margin": "0 0 24px", "line-height": "1.1", "letter-spacing": "-.03em"}, "content": "Capturing Moments\nThat Last Forever"},
                     {"tagName": "p", "style": {"font-size": "1.1rem", "color": "#71717a", "margin": "0 auto 48px", "max-width": "480px", "line-height": "1.7"}, "content": "Weddings, portraits, corporate events — every shot tells a story worth remembering."},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#gallery"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#fafafa", "color": "#18181b", "text-decoration": "none", "font-weight": "700"}, "content": "View Portfolio"},
                          {"tagName": "a", "attributes": {"href": "#book"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "1px solid #52525b", "color": "#fafafa", "text-decoration": "none", "font-weight": "600"}, "content": "Book a Session"},
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "gallery"}, "style": {"padding": "80px 48px", "background": "#09090b"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "300", "color": "#fafafa", "margin": "0 0 48px", "letter-spacing": "-.02em"}, "content": "Portfolio"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "4px", "max-width": "1000px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"height": "260px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "4rem", "cursor": "pointer"},
                             "content": ic} for ic, c1, c2 in [
                              ("💍", "#27272a", "#3f3f46"),
                              ("👨‍👩‍👧‍👦", "#1c1917", "#292524"),
                              ("🌆", "#0c0a09", "#1c1917"),
                              ("👰", "#27272a", "#52525b"),
                              ("🎂", "#18181b", "#3f3f46"),
                              ("🌿", "#14532d", "#166534"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "services"}, "style": {"padding": "80px 48px", "background": "#18181b"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "300", "color": "#fafafa", "margin": "0 0 48px"}, "content": "Services & Pricing"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "1px", "max-width": "900px", "margin": "0 auto", "background": "#27272a"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "40px 28px", "background": "#18181b", "text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2rem", "margin-bottom": "16px"}, "content": ic},
                                 {"tagName": "h3", "style": {"font-size": "1rem", "font-weight": "600", "color": "#fafafa", "margin": "0 0 8px"}, "content": nm},
                                 {"tagName": "p", "style": {"color": "#71717a", "font-size": ".85rem", "margin": "0 0 20px", "line-height": "1.6"}, "content": desc},
                                 {"tagName": "div", "style": {"font-size": "1.5rem", "font-weight": "700", "color": "#fafafa"}, "content": pr},
                             ]} for ic, nm, desc, pr in [
                              ("💍", "Wedding", "Full-day coverage, 500+ edited photos, album", "From $2,500"),
                              ("🤳", "Portrait", "2-hour studio session, 30 edited photos", "From $350"),
                              ("🏢", "Corporate", "Events, headshots, brand photography", "From $800"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "book"}, "style": {"padding": "80px 48px", "background": "#09090b", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "300", "color": "#fafafa", "margin": "0 0 12px", "letter-spacing": "-.02em"}, "content": "Let's Create Together"},
                     {"tagName": "p", "style": {"color": "#71717a", "margin": "0 0 36px", "font-size": "1rem"}, "content": "Limited availability — book early to secure your date"},
                     {"tagName": "a", "attributes": {"href": "mailto:hello@lensandlight.com"}, "style": {"display": "inline-block", "padding": "14px 40px", "background": "#fafafa", "color": "#18181b", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "✉ hello@lensandlight.com"},
                 ]},
                {"tagName": "footer", "style": {"background": "#09090b", "color": "#52525b", "padding": "28px 48px", "text-align": "center", "border-top": "1px solid #27272a"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".8rem"}, "content": "© 2025 Lens & Light Photography. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 13. E-Commerce Store
    # ─────────────────────────────────────────────
    {
        "name": "E-Commerce Store",
        "slug": "ecommerce-store",
        "category": "ecommerce",
        "description": "متجر إلكتروني مع عرض المنتجات والتصنيفات وأزرار الشراء",
        "is_featured": True,
        "theme_vars": {
            "primary_color": "#f97316",
            "secondary_color": "#ea580c",
            "accent_color": "#0f172a",
            "background_color": "#fff",
            "text_color": "#0f172a",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "8px",
        },
        "thumbnail_url": "/static/templates/ecommerce.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "div", "style": {"background": "#f97316", "padding": "8px 48px", "text-align": "center"},
                 "components": [{"tagName": "span", "style": {"color": "#fff", "font-size": ".85rem", "font-weight": "600"}, "content": "🎉 Free shipping on orders over $50 — Use code FREESHIP"}]},
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#fff", "box-shadow": "0 1px 4px rgba(0,0,0,.08)", "position": "sticky", "top": "0", "z-index": "100"},
                 "components": [
                     {"tagName": "div", "style": {"font-size": "1.5rem", "font-weight": "800", "color": "#f97316"}, "content": "🛍 ShopZone"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "24px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#categories"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Categories"},
                          {"tagName": "a", "attributes": {"href": "#products"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Products"},
                          {"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#f97316", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "700"}, "content": "🛒 Cart (0)"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "80px 48px", "background": "linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)", "display": "flex", "align-items": "center", "gap": "60px"},
                 "components": [
                     {"tagName": "div", "style": {"flex": "1"},
                      "components": [
                          {"tagName": "span", "style": {"display": "inline-block", "background": "#f97316", "color": "#fff", "padding": "5px 14px", "border-radius": "20px", "font-size": ".75rem", "font-weight": "700", "margin-bottom": "16px"}, "content": "⚡ FLASH SALE — Up to 50% OFF"},
                          {"tagName": "h1", "style": {"font-size": "3rem", "font-weight": "800", "color": "#0f172a", "margin": "0 0 16px", "line-height": "1.2"}, "content": "Shop the Latest Trends"},
                          {"tagName": "p", "style": {"font-size": "1.1rem", "color": "#64748b", "line-height": "1.7", "margin": "0 0 36px", "max-width": "460px"}, "content": "Thousands of products — fashion, electronics, home & more — delivered to your door."},
                          {"tagName": "div", "style": {"display": "flex", "gap": "16px"},
                           "components": [
                               {"tagName": "a", "attributes": {"href": "#products"}, "style": {"display": "inline-block", "padding": "13px 32px", "background": "#f97316", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "Shop Now"},
                               {"tagName": "a", "attributes": {"href": "#categories"}, "style": {"display": "inline-block", "padding": "13px 32px", "border": "2px solid #f97316", "color": "#f97316", "border-radius": "8px", "text-decoration": "none", "font-weight": "700"}, "content": "View Categories"},
                           ]},
                      ]},
                     {"tagName": "div", "style": {"flex": "1", "background": "#fff", "border-radius": "16px", "padding": "32px", "box-shadow": "0 8px 32px rgba(249,115,22,.1)", "text-align": "center"},
                      "components": [
                          {"tagName": "div", "style": {"font-size": "6rem", "margin-bottom": "16px"}, "content": "🎁"},
                          {"tagName": "div", "style": {"font-size": "1.1rem", "font-weight": "700", "color": "#0f172a"}, "content": "New Arrivals Every Week"},
                          {"tagName": "div", "style": {"color": "#64748b", "font-size": ".9rem", "margin-top": "8px"}, "content": "Fresh picks just landed in store"},
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "categories"}, "style": {"padding": "60px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 36px"}, "content": "Shop by Category"},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center", "flex-wrap": "wrap"},
                      "components": [
                          *[{"tagName": "a", "attributes": {"href": "#products"}, "style": {"display": "flex", "flex-direction": "column", "align-items": "center", "padding": "20px 24px", "background": bg, "border-radius": "12px", "text-decoration": "none", "min-width": "100px"},
                             "components": [
                                 {"tagName": "span", "style": {"font-size": "2rem", "margin-bottom": "8px"}, "content": ic},
                                 {"tagName": "span", "style": {"font-size": ".85rem", "font-weight": "600", "color": "#0f172a"}, "content": nm},
                             ]} for ic, nm, bg in [
                              ("👗", "Fashion", "#fff7ed"),
                              ("📱", "Electronics", "#eff6ff"),
                              ("🏠", "Home", "#f0fdf4"),
                              ("💄", "Beauty", "#fdf2f8"),
                              ("⚽", "Sports", "#ecfdf5"),
                              ("📚", "Books", "#faf5ff"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "products"}, "style": {"padding": "60px 48px", "background": "#f8fafc"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "700", "color": "#0f172a", "margin": "0 0 36px"}, "content": "Featured Products"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(4, 1fr)", "gap": "20px", "max-width": "1100px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"background": "#fff", "border-radius": "12px", "overflow": "hidden", "box-shadow": "0 2px 8px rgba(0,0,0,.06)", "transition": "box-shadow .2s"},
                             "components": [
                                 {"tagName": "div", "style": {"height": "180px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "3.5rem", "position": "relative"},
                                  "components": [
                                      {"tagName": "div", "content": ic},
                                      {"tagName": "span", "style": {"position": "absolute", "top": "10px", "right": "10px", "background": "#dc2626", "color": "#fff", "padding": "2px 8px", "border-radius": "4px", "font-size": ".7rem", "font-weight": "700"}, "content": badge},
                                  ]},
                                 {"tagName": "div", "style": {"padding": "14px"},
                                  "components": [
                                      {"tagName": "h3", "style": {"font-size": ".9rem", "font-weight": "600", "color": "#0f172a", "margin": "0 0 6px"}, "content": nm},
                                      {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center", "margin-bottom": "10px"},
                                       "components": [
                                           {"tagName": "span", "style": {"font-size": "1.1rem", "font-weight": "800", "color": "#f97316"}, "content": pr},
                                           {"tagName": "span", "style": {"font-size": ".8rem", "color": "#94a3b8", "text-decoration": "line-through"}, "content": old},
                                       ]},
                                      {"tagName": "button", "style": {"width": "100%", "padding": "8px", "background": "#f97316", "color": "#fff", "border": "none", "border-radius": "6px", "font-weight": "700", "font-size": ".85rem", "cursor": "pointer"}, "content": "Add to Cart"},
                                  ]},
                             ]} for ic, nm, pr, old, badge, c1, c2 in [
                              ("👟", "Air Max Sneakers", "$89", "$120", "-25%", "#fff7ed", "#ffedd5"),
                              ("⌚", "Smart Watch Pro", "$199", "$280", "-30%", "#eff6ff", "#dbeafe"),
                              ("🎧", "Wireless Earbuds", "$59", "$90", "-35%", "#f0fdf4", "#dcfce7"),
                              ("💻", "Laptop Stand", "$39", "$55", "-29%", "#faf5ff", "#ede9fe"),
                          ]],
                      ]},
                 ]},
                {"tagName": "footer", "style": {"background": "#0f172a", "color": "#64748b", "padding": "40px 48px"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center", "flex-wrap": "wrap", "gap": "20px"},
                      "components": [
                          {"tagName": "div", "style": {"font-size": "1.25rem", "font-weight": "800", "color": "#f97316"}, "content": "🛍 ShopZone"},
                          {"tagName": "div", "style": {"font-size": ".85rem"}, "content": "© 2025 ShopZone. All rights reserved."},
                          {"tagName": "div", "style": {"display": "flex", "gap": "16px"},
                           "components": [
                               {"tagName": "span", "style": {"font-size": "1.2rem"}, "content": icon} for icon in ["💳", "📦", "🔒", "🔄"]
                           ]},
                      ]},
                 ]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 14. Wedding & Events
    # ─────────────────────────────────────────────
    {
        "name": "Wedding & Events",
        "slug": "wedding-events",
        "category": "events",
        "description": "موقع أفراح وفعاليات أنيق مع عرض الباقات والمعرض والتواصل",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#be8a6d",
            "secondary_color": "#a87050",
            "accent_color": "#f5f0eb",
            "background_color": "#fdf8f4",
            "text_color": "#2c1810",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "0px",
        },
        "thumbnail_url": "/static/templates/wedding.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "20px 60px", "background": "#fdf8f4", "border-bottom": "1px solid #f0e6da"},
                 "components": [
                     {"tagName": "div", "style": {"text-align": "center"},
                      "components": [
                          {"tagName": "div", "style": {"font-size": "1.1rem", "font-weight": "300", "letter-spacing": ".25em", "color": "#2c1810", "text-transform": "uppercase"}, "content": "Eternal Moments"},
                          {"tagName": "div", "style": {"font-size": ".65rem", "letter-spacing": ".15em", "color": "#be8a6d", "text-transform": "uppercase"}, "content": "Wedding & Event Planners"},
                      ]},
                     {"tagName": "div", "style": {"display": "flex", "gap": "36px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#gallery"}, "style": {"color": "#6b4226", "text-decoration": "none", "font-size": ".85rem", "letter-spacing": ".05em"}, "content": "Gallery"},
                          {"tagName": "a", "attributes": {"href": "#packages"}, "style": {"color": "#6b4226", "text-decoration": "none", "font-size": ".85rem", "letter-spacing": ".05em"}, "content": "Packages"},
                          {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "10px 28px", "background": "#be8a6d", "color": "#fff", "text-decoration": "none", "font-size": ".85rem", "letter-spacing": ".05em"}, "content": "Inquire Now"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "140px 60px", "background": "linear-gradient(rgba(253,248,244,.6),rgba(253,248,244,.6)), url('https://images.unsplash.com/photo-1519741497674-611481863552?w=1600') center/cover", "text-align": "center"},
                 "components": [
                     {"tagName": "p", "style": {"font-size": ".75rem", "letter-spacing": ".25em", "color": "#be8a6d", "text-transform": "uppercase", "margin": "0 0 20px"}, "content": "— Your Special Day —"},
                     {"tagName": "h1", "style": {"font-size": "3.5rem", "font-weight": "300", "color": "#2c1810", "margin": "0 0 24px", "line-height": "1.2", "letter-spacing": "-.01em"}, "content": "Love Stories Deserve\nPerfect Celebrations"},
                     {"tagName": "p", "style": {"font-size": "1.05rem", "color": "#6b4226", "margin": "0 auto 48px", "max-width": "500px", "line-height": "1.8"}, "content": "We craft unforgettable weddings and events, tailored to your vision — from intimate gatherings to grand celebrations."},
                     {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "14px 44px", "background": "#be8a6d", "color": "#fff", "text-decoration": "none", "font-weight": "400", "font-size": "1rem", "letter-spacing": ".08em"}, "content": "START PLANNING"},
                 ]},
                {"tagName": "section", "attributes": {"id": "gallery"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "300", "color": "#2c1810", "margin": "0 0 8px", "letter-spacing": ".05em"}, "content": "Our Gallery"},
                     {"tagName": "p", "style": {"text-align": "center", "color": "#be8a6d", "margin": "0 auto 48px", "letter-spacing": ".08em", "font-size": ".8rem", "text-transform": "uppercase"}, "content": "— A Few Precious Moments —"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "8px", "max-width": "1000px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"height": "240px", "background": f"linear-gradient(135deg, {c1}, {c2})", "display": "flex", "align-items": "center", "justify-content": "center", "font-size": "4rem"}, "content": ic}
                            for ic, c1, c2 in [
                              ("💐", "#fdf2f8", "#fce7f3"),
                              ("🕊️", "#f0f9ff", "#e0f2fe"),
                              ("🍰", "#fff7ed", "#ffedd5"),
                              ("💍", "#fdf4ff", "#f3e8ff"),
                              ("🌹", "#fef2f2", "#fee2e2"),
                              ("🥂", "#fefce8", "#fef9c3"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "packages"}, "style": {"padding": "80px 48px", "background": "#fdf8f4"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2rem", "font-weight": "300", "color": "#2c1810", "margin": "0 0 48px"}, "content": "Wedding Packages"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "1px", "max-width": "900px", "margin": "0 auto", "background": "#e8d5c4"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "40px 28px", "background": bg, "text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": ".7rem", "letter-spacing": ".2em", "color": "#be8a6d", "text-transform": "uppercase", "margin-bottom": "12px"}, "content": plan},
                                 {"tagName": "div", "style": {"font-size": "2.5rem", "font-weight": "300", "color": "#2c1810", "margin": "0 0 8px"}, "content": price},
                                 {"tagName": "p", "style": {"color": "#6b4226", "font-size": ".85rem", "line-height": "1.7", "margin": "0 0 28px"}, "content": feat},
                                 {"tagName": "a", "attributes": {"href": "#contact"}, "style": {"display": "inline-block", "padding": "10px 28px", "background": "#be8a6d", "color": "#fff", "text-decoration": "none", "font-size": ".85rem", "letter-spacing": ".05em"}, "content": "Choose Plan"},
                             ]} for plan, price, feat, bg in [
                              ("Intimate", "$3,500", "Up to 50 guests\nFloral arrangement\nPhotography 4hrs", "#fff"),
                              ("Classic", "$7,500", "Up to 150 guests\nFull decoration\nPhotography + Video", "#fdf8f4"),
                              ("Grand", "$15,000", "Up to 400 guests\nLuxury decor & catering\nFull media coverage", "#fff"),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "contact"}, "style": {"padding": "80px 60px", "background": "#2c1810", "text-align": "center"},
                 "components": [
                     {"tagName": "p", "style": {"font-size": ".75rem", "letter-spacing": ".25em", "color": "#be8a6d", "text-transform": "uppercase", "margin": "0 0 16px"}, "content": "— Let's Talk —"},
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "300", "color": "#fff", "margin": "0 0 12px"}, "content": "Begin Your Love Story"},
                     {"tagName": "p", "style": {"color": "#be8a6d", "margin": "0 0 36px"}, "content": "Free consultation — we'd love to hear your vision"},
                     {"tagName": "a", "attributes": {"href": "mailto:hello@eternalmoments.com"}, "style": {"display": "inline-block", "padding": "13px 40px", "border": "1px solid #be8a6d", "color": "#be8a6d", "text-decoration": "none", "letter-spacing": ".08em", "font-size": ".9rem"}, "content": "✉ SEND US A MESSAGE"},
                 ]},
                {"tagName": "footer", "style": {"background": "#1a0e08", "color": "#6b4226", "padding": "28px 60px", "text-align": "center"},
                 "components": [{"tagName": "p", "style": {"margin": "0", "font-size": ".8rem", "letter-spacing": ".05em"}, "content": "© 2025 Eternal Moments. All rights reserved."}]},
            ]}}],
            "styles": []
        }
    },

    # ─────────────────────────────────────────────
    # 15. Nonprofit / Charity
    # ─────────────────────────────────────────────
    {
        "name": "Nonprofit / Charity",
        "slug": "nonprofit-charity",
        "category": "nonprofit",
        "description": "موقع منظمة خيرية وغير ربحية مع عرض البرامج وجمع التبرعات",
        "is_featured": False,
        "theme_vars": {
            "primary_color": "#16a34a",
            "secondary_color": "#15803d",
            "accent_color": "#f59e0b",
            "background_color": "#f0fdf4",
            "text_color": "#14532d",
            "heading_font": "Inter",
            "body_font": "Inter",
            "border_radius": "8px",
        },
        "thumbnail_url": "/static/templates/nonprofit.png",
        "grapes_data": {
            "pages": [{"id": "main", "component": {"type": "wrapper", "components": [
                {"tagName": "nav", "style": {"display": "flex", "align-items": "center", "justify-content": "space-between", "padding": "16px 48px", "background": "#fff", "box-shadow": "0 1px 4px rgba(0,0,0,.06)", "position": "sticky", "top": "0", "z-index": "100"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "align-items": "center", "gap": "10px"},
                      "components": [
                          {"tagName": "span", "style": {"font-size": "1.5rem"}, "content": "🌱"},
                          {"tagName": "span", "style": {"font-size": "1.2rem", "font-weight": "800", "color": "#16a34a"}, "content": "HopeBridge"},
                      ]},
                     {"tagName": "div", "style": {"display": "flex", "gap": "28px", "align-items": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#programs"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Programs"},
                          {"tagName": "a", "attributes": {"href": "#impact"}, "style": {"color": "#475569", "text-decoration": "none", "font-size": ".9rem"}, "content": "Our Impact"},
                          {"tagName": "a", "attributes": {"href": "#donate"}, "style": {"display": "inline-block", "padding": "9px 22px", "background": "#f59e0b", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-size": ".9rem", "font-weight": "700"}, "content": "❤️ Donate Now"},
                      ]},
                 ]},
                {"tagName": "section", "style": {"padding": "100px 48px", "background": "linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)", "text-align": "center"},
                 "components": [
                     {"tagName": "span", "style": {"display": "inline-block", "background": "#16a34a", "color": "#fff", "padding": "6px 16px", "border-radius": "20px", "font-size": ".8rem", "font-weight": "600", "margin-bottom": "20px"}, "content": "Making a Difference Since 2005"},
                     {"tagName": "h1", "style": {"font-size": "3.5rem", "font-weight": "800", "color": "#14532d", "margin": "0 0 20px", "line-height": "1.15"}, "content": "Together We Build\nA Better Tomorrow"},
                     {"tagName": "p", "style": {"font-size": "1.15rem", "color": "#166534", "margin": "0 auto 40px", "max-width": "560px", "line-height": "1.7"}, "content": "We provide education, clean water, and healthcare to communities in need. Every contribution creates lasting change."},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center"},
                      "components": [
                          {"tagName": "a", "attributes": {"href": "#donate"}, "style": {"display": "inline-block", "padding": "14px 36px", "background": "#f59e0b", "color": "#fff", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "❤️ Donate Now"},
                          {"tagName": "a", "attributes": {"href": "#programs"}, "style": {"display": "inline-block", "padding": "14px 36px", "border": "2px solid #16a34a", "color": "#16a34a", "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem"}, "content": "Our Work"},
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "impact"}, "style": {"padding": "60px 48px", "background": "#16a34a"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "gap": "48px", "justify-content": "center", "max-width": "900px", "margin": "0 auto", "flex-wrap": "wrap"},
                      "components": [
                          *[{"tagName": "div", "style": {"text-align": "center"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2.25rem", "font-weight": "800", "color": "#fff"}, "content": num},
                                 {"tagName": "div", "style": {"font-size": ".85rem", "color": "#bbf7d0", "margin-top": "4px"}, "content": lbl},
                             ]} for num, lbl in [("150K+", "Lives Impacted"), ("800+", "Clean Water Wells"), ("200+", "Schools Built"), ("50+", "Countries Reached")]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "programs"}, "style": {"padding": "80px 48px", "background": "#fff"},
                 "components": [
                     {"tagName": "h2", "style": {"text-align": "center", "font-size": "2.25rem", "font-weight": "700", "color": "#14532d", "margin": "0 0 48px"}, "content": "Our Programs"},
                     {"tagName": "div", "style": {"display": "grid", "grid-template-columns": "repeat(3, 1fr)", "gap": "28px", "max-width": "1000px", "margin": "0 auto"},
                      "components": [
                          *[{"tagName": "div", "style": {"padding": "36px 28px", "border-top": "4px solid #16a34a", "box-shadow": "0 4px 16px rgba(0,0,0,.06)", "border-radius": "0 0 12px 12px"},
                             "components": [
                                 {"tagName": "div", "style": {"font-size": "2.5rem", "margin-bottom": "16px"}, "content": ic},
                                 {"tagName": "h3", "style": {"font-size": "1.15rem", "font-weight": "700", "color": "#14532d", "margin": "0 0 12px"}, "content": nm},
                                 {"tagName": "p", "style": {"color": "#64748b", "font-size": ".9rem", "line-height": "1.6", "margin": "0 0 20px"}, "content": desc},
                                 {"tagName": "a", "attributes": {"href": "#donate"}, "style": {"color": "#16a34a", "font-weight": "600", "font-size": ".9rem", "text-decoration": "none"}, "content": "Support this program →"},
                             ]} for ic, nm, desc in [
                              ("📚", "Education for All", "We build schools and provide scholarships to 50,000+ students annually in underserved regions."),
                              ("💧", "Clean Water Access", "Installing wells and water purification systems in villages without safe drinking water."),
                              ("🏥", "Healthcare Outreach", "Mobile clinics providing free medical care, vaccines, and maternal health support."),
                          ]],
                      ]},
                 ]},
                {"tagName": "section", "attributes": {"id": "donate"}, "style": {"padding": "80px 48px", "background": "#f0fdf4", "text-align": "center"},
                 "components": [
                     {"tagName": "h2", "style": {"font-size": "2.25rem", "font-weight": "700", "color": "#14532d", "margin": "0 0 12px"}, "content": "Make a Difference Today"},
                     {"tagName": "p", "style": {"color": "#166534", "margin": "0 0 36px", "font-size": "1.05rem"}, "content": "100% of your donation goes directly to our programs."},
                     {"tagName": "div", "style": {"display": "flex", "gap": "16px", "justify-content": "center", "flex-wrap": "wrap"},
                      "components": [
                          *[{"tagName": "a", "attributes": {"href": "#"}, "style": {"display": "inline-block", "padding": "14px 28px", "background": bg, "color": tc, "border-radius": "8px", "text-decoration": "none", "font-weight": "700", "font-size": "1rem", "border": brd},
                             "content": lbl} for lbl, bg, tc, brd in [
                              ("$10 / month", "#fff", "#16a34a", "2px solid #16a34a"),
                              ("$25 / month", "#16a34a", "#fff", "none"),
                              ("$50 / month", "#14532d", "#fff", "none"),
                              ("Custom Amount", "#f59e0b", "#fff", "none"),
                          ]],
                      ]},
                 ]},
                {"tagName": "footer", "style": {"background": "#14532d", "color": "#86efac", "padding": "36px 48px"},
                 "components": [
                     {"tagName": "div", "style": {"display": "flex", "justify-content": "space-between", "align-items": "center", "flex-wrap": "wrap", "gap": "16px"},
                      "components": [
                          {"tagName": "span", "style": {"font-size": "1.1rem", "font-weight": "700", "color": "#fff"}, "content": "🌱 HopeBridge"},
                          {"tagName": "span", "style": {"font-size": ".85rem"}, "content": "© 2025 HopeBridge Foundation. Registered nonprofit."},
                      ]},
                 ]},
            ]}}],
            "styles": []
        }
    },
]


def seed_templates(db: Session):
    """Seed templates — insert any new ones not already in DB."""
    existing_slugs = {row.slug for row in db.query(Template.slug).all()}

    added = 0
    for t in TEMPLATES:
        if t["slug"] not in existing_slugs:
            db.add(Template(**t))
            added += 1

    if added:
        db.commit()
        print(f"[seed] Inserted {added} new templates")
