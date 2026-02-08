#!/usr/bin/env python3
"""
Project Analysis Script for Agent Teams
分析项目结构和技术栈，为团队配置提供智能建议
"""

import os
import json
import glob
import re
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
from dataclasses import dataclass, asdict
from collections import Counter

@dataclass
class ProjectAnalysis:
    """项目分析结果"""
    project_type: str
    primary_language: str
    frameworks: List[str]
    project_structure: str
    test_coverage: float
    dependencies: Dict[str, List[str]]
    file_stats: Dict[str, int]
    complexity_score: int
    suggested_team_size: int
    suggested_roles: List[str]
    parallelization_opportunities: List[str]
    risk_areas: List[str]

class ProjectAnalyzer:
    """项目分析器"""

    def __init__(self, project_path: str):
        self.project_path = Path(project_path)
        self.file_extensions = Counter()
        self.frameworks = set()
        self.dependencies = {
            'frontend': [],
            'backend': [],
            'devops': [],
            'testing': []
        }

    def analyze(self) -> ProjectAnalysis:
        """执行完整的项目分析"""
        self._scan_files()
        project_type = self._detect_project_type()
        primary_language = self._detect_primary_language()
        frameworks = self._detect_frameworks()
        structure = self._analyze_structure()
        test_coverage = self._estimate_test_coverage()
        complexity = self._calculate_complexity()
        team_config = self._suggest_team_configuration(complexity, project_type)

        return ProjectAnalysis(
            project_type=project_type,
            primary_language=primary_language,
            frameworks=list(frameworks),
            project_structure=structure,
            test_coverage=test_coverage,
            dependencies=self.dependencies,
            file_stats=dict(self.file_extensions),
            complexity_score=complexity,
            suggested_team_size=team_config['size'],
            suggested_roles=team_config['roles'],
            parallelization_opportunities=self._find_parallelization_opportunities(),
            risk_areas=self._identify_risk_areas()
        )

    def _scan_files(self):
        """扫描所有文件并统计"""
        for file_path in self.project_path.rglob('*'):
            if file_path.is_file() and not self._should_ignore(file_path):
                ext = file_path.suffix
                self.file_extensions[ext] += 1

    def _should_ignore(self, path: Path) -> bool:
        """检查是否应忽略该文件"""
        ignore_dirs = {
            'node_modules', '.git', '__pycache__', 'dist', 'build',
            '.next', 'coverage', '.pytest_cache', 'venv', '.env'
        }
        return any(part in ignore_dirs for part in path.parts)

    def _detect_project_type(self) -> str:
        """检测项目类型"""
        indicators = {
            'web-fullstack': ['package.json', 'index.html', 'server.js'],
            'web-frontend': ['package.json', 'index.html', 'src/App.js'],
            'web-backend': ['server.js', 'app.py', 'main.go'],
            'mobile': ['ios/', 'android/', 'flutter.yaml'],
            'desktop': ['electron.js', 'main.cpp', 'main.swift'],
            'cli': ['cli.js', 'main.py', 'Cargo.toml'],
            'library': ['lib/', 'index.d.ts', 'setup.py'],
            'microservices': ['docker-compose.yml', 'services/', 'k8s/'],
            'monorepo': ['lerna.json', 'nx.json', 'packages/']
        }

        for proj_type, files in indicators.items():
            if any((self.project_path / f).exists() for f in files):
                return proj_type

        return 'general'

    def _detect_primary_language(self) -> str:
        """检测主要编程语言"""
        language_extensions = {
            '.js': 'JavaScript',
            '.ts': 'TypeScript',
            '.jsx': 'React',
            '.tsx': 'TypeScript/React',
            '.py': 'Python',
            '.go': 'Go',
            '.rs': 'Rust',
            '.java': 'Java',
            '.cpp': 'C++',
            '.cs': 'C#',
            '.rb': 'Ruby',
            '.php': 'PHP',
            '.swift': 'Swift',
            '.kt': 'Kotlin'
        }

        # 找出最常见的编程语言文件
        lang_counts = {}
        for ext, count in self.file_extensions.items():
            if ext in language_extensions:
                lang = language_extensions[ext]
                lang_counts[lang] = lang_counts.get(lang, 0) + count

        if lang_counts:
            return max(lang_counts, key=lang_counts.get)
        return 'Unknown'

    def _detect_frameworks(self) -> Set[str]:
        """检测使用的框架"""
        frameworks = set()

        # 检查 package.json
        package_json = self.project_path / 'package.json'
        if package_json.exists():
            try:
                with open(package_json) as f:
                    data = json.load(f)
                    deps = {**data.get('dependencies', {}), **data.get('devDependencies', {})}

                    framework_map = {
                        'react': 'React',
                        'vue': 'Vue',
                        'angular': 'Angular',
                        'next': 'Next.js',
                        'nuxt': 'Nuxt',
                        'express': 'Express',
                        'fastify': 'Fastify',
                        'nest': 'NestJS',
                        'jest': 'Jest',
                        'mocha': 'Mocha',
                        'playwright': 'Playwright',
                        'cypress': 'Cypress'
                    }

                    for key, framework in framework_map.items():
                        if key in deps:
                            frameworks.add(framework)
                            self._categorize_dependency(framework)

            except json.JSONDecodeError:
                pass

        # 检查 Python 项目
        requirements = self.project_path / 'requirements.txt'
        if requirements.exists():
            with open(requirements) as f:
                content = f.read()
                python_frameworks = {
                    'django': 'Django',
                    'flask': 'Flask',
                    'fastapi': 'FastAPI',
                    'pytest': 'Pytest',
                    'numpy': 'NumPy',
                    'pandas': 'Pandas',
                    'tensorflow': 'TensorFlow',
                    'torch': 'PyTorch'
                }
                for key, framework in python_frameworks.items():
                    if key in content.lower():
                        frameworks.add(framework)
                        self._categorize_dependency(framework)

        self.frameworks = frameworks
        return frameworks

    def _categorize_dependency(self, framework: str):
        """将框架分类到相应的依赖类别"""
        categories = {
            'frontend': ['React', 'Vue', 'Angular', 'Next.js', 'Nuxt'],
            'backend': ['Express', 'Fastify', 'NestJS', 'Django', 'Flask', 'FastAPI'],
            'testing': ['Jest', 'Mocha', 'Playwright', 'Cypress', 'Pytest'],
            'devops': ['Docker', 'Kubernetes', 'Terraform']
        }

        for category, frameworks in categories.items():
            if framework in frameworks:
                self.dependencies[category].append(framework)

    def _analyze_structure(self) -> str:
        """分析项目结构"""
        structures = []

        # 检查常见的项目结构
        if (self.project_path / 'src').exists():
            structures.append('src-based')
        if (self.project_path / 'packages').exists():
            structures.append('monorepo')
        if (self.project_path / 'services').exists():
            structures.append('microservices')
        if (self.project_path / 'apps').exists():
            structures.append('multi-app')

        # 检查分层架构
        common_dirs = ['controllers', 'models', 'views', 'services', 'repositories']
        if sum(1 for d in common_dirs if (self.project_path / d).exists()) >= 3:
            structures.append('mvc/layered')

        return ', '.join(structures) if structures else 'flat'

    def _estimate_test_coverage(self) -> float:
        """估算测试覆盖率"""
        test_files = 0
        source_files = 0

        for ext in ['.js', '.ts', '.py', '.go', '.java']:
            source_files += self.file_extensions.get(ext, 0)

        for pattern in ['*.test.*', '*.spec.*', 'test_*.py', '*_test.go']:
            test_files += len(list(self.project_path.rglob(pattern)))

        if source_files > 0:
            return min(100.0, (test_files / source_files) * 100)
        return 0.0

    def _calculate_complexity(self) -> int:
        """计算项目复杂度（1-10分）"""
        score = 1

        # 基于文件数量
        total_files = sum(self.file_extensions.values())
        if total_files > 1000:
            score += 3
        elif total_files > 500:
            score += 2
        elif total_files > 100:
            score += 1

        # 基于框架数量
        if len(self.frameworks) > 5:
            score += 2
        elif len(self.frameworks) > 3:
            score += 1

        # 基于项目类型
        complex_types = ['microservices', 'monorepo', 'web-fullstack']
        if self._detect_project_type() in complex_types:
            score += 2

        # 基于依赖复杂度
        total_deps = sum(len(deps) for deps in self.dependencies.values())
        if total_deps > 10:
            score += 1

        return min(10, score)

    def _suggest_team_configuration(self, complexity: int, project_type: str) -> Dict:
        """建议团队配置"""
        base_roles = ['product-manager', 'tech-lead', 'qa-engineer']

        # 基于项目类型添加角色
        type_roles = {
            'web-fullstack': ['frontend-developer', 'backend-developer', 'ux-designer', 'devops-engineer'],
            'web-frontend': ['frontend-developer', 'ux-designer', 'frontend-architect'],
            'web-backend': ['backend-developer', 'database-engineer', 'devops-engineer'],
            'mobile': ['mobile-developer', 'ux-designer', 'backend-developer'],
            'microservices': ['backend-developer', 'devops-engineer', 'system-architect', 'database-engineer'],
            'monorepo': ['frontend-developer', 'backend-developer', 'devops-engineer', 'build-engineer']
        }

        roles = base_roles + type_roles.get(project_type, ['full-stack-developer'])

        # 基于复杂度调整团队规模
        if complexity <= 3:
            size = 3-4
            roles = roles[:4]
        elif complexity <= 6:
            size = 5-7
            roles = roles[:7]
        else:
            size = 8-12
            # 高复杂度项目添加额外角色
            roles.extend(['security-engineer', 'performance-engineer', 'technical-writer'])

        # 添加领导角色
        if complexity > 7:
            roles.insert(0, 'cto')
            roles.insert(0, 'ceo')

        return {
            'size': size,
            'roles': list(set(roles))  # 去重
        }

    def _find_parallelization_opportunities(self) -> List[str]:
        """查找可并行化的机会"""
        opportunities = []

        # 检查独立的模块/服务
        if (self.project_path / 'packages').exists():
            packages = [d.name for d in (self.project_path / 'packages').iterdir() if d.is_dir()]
            if packages:
                opportunities.append(f"Independent packages: {', '.join(packages[:5])}")

        if (self.project_path / 'services').exists():
            services = [d.name for d in (self.project_path / 'services').iterdir() if d.is_dir()]
            if services:
                opportunities.append(f"Independent services: {', '.join(services[:5])}")

        # 前后端分离
        if 'React' in self.frameworks and any(f in self.frameworks for f in ['Express', 'Django', 'Flask']):
            opportunities.append("Frontend and backend can be developed in parallel")

        # 测试可以并行
        if self._estimate_test_coverage() > 0:
            opportunities.append("Test development can run parallel to feature development")

        # 文档可以并行
        if (self.project_path / 'docs').exists():
            opportunities.append("Documentation can be updated in parallel")

        return opportunities

    def _identify_risk_areas(self) -> List[str]:
        """识别风险区域"""
        risks = []

        # 低测试覆盖率
        coverage = self._estimate_test_coverage()
        if coverage < 30:
            risks.append(f"Low test coverage ({coverage:.1f}%)")

        # 缺少关键文件
        critical_files = ['README.md', '.gitignore', 'package.json', 'requirements.txt']
        missing = [f for f in critical_files if not (self.project_path / f).exists()]
        if missing:
            risks.append(f"Missing critical files: {', '.join(missing)}")

        # 复杂依赖
        if len(self.dependencies['frontend']) > 5 or len(self.dependencies['backend']) > 5:
            risks.append("Complex dependency tree may cause conflicts")

        # 缺少 CI/CD
        if not any((self.project_path / ci).exists() for ci in ['.github/workflows', '.gitlab-ci.yml', 'Jenkinsfile']):
            risks.append("No CI/CD configuration detected")

        # 安全配置
        if (self.project_path / '.env').exists():
            risks.append(".env file in repository (potential security risk)")

        return risks

def generate_team_recommendation(analysis: ProjectAnalysis) -> Dict:
    """基于分析结果生成团队推荐"""
    recommendation = {
        'team_size': analysis.suggested_team_size,
        'topology': 'hub-spoke' if analysis.complexity_score > 7 else 'flat',
        'methodology': 'agile-scrum' if analysis.complexity_score > 5 else 'kanban',
        'roles': []
    }

    # 为每个建议的角色分配模型
    model_assignment = {
        'ceo': 'opus',
        'cto': 'opus',
        'tech-lead': 'opus',
        'product-manager': 'sonnet',
        'system-architect': 'sonnet',
        'frontend-architect': 'sonnet',
        'backend-architect': 'sonnet'
    }

    for role in analysis.suggested_roles:
        model = model_assignment.get(role, 'sonnet' if 'developer' in role else 'haiku')
        recommendation['roles'].append({
            'role': role,
            'model': model,
            'count': 2 if role.endswith('developer') and analysis.complexity_score > 7 else 1
        })

    # 添加工作流建议
    recommendation['workflow'] = {
        'phases': [],
        'parallelization': analysis.parallelization_opportunities
    }

    if analysis.project_type == 'web-fullstack':
        recommendation['workflow']['phases'] = [
            'requirements', 'design', 'parallel(frontend,backend)', 'integration', 'testing', 'deployment'
        ]
    else:
        recommendation['workflow']['phases'] = [
            'requirements', 'design', 'development', 'testing', 'deployment'
        ]

    return recommendation

def main(project_path: str = '.'):
    """主函数"""
    print(f"\n🔍 Analyzing project: {project_path}\n")
    print("=" * 60)

    analyzer = ProjectAnalyzer(project_path)
    analysis = analyzer.analyze()

    # 打印分析结果
    print(f"\n📊 Project Analysis Results:")
    print(f"  • Project Type: {analysis.project_type}")
    print(f"  • Primary Language: {analysis.primary_language}")
    print(f"  • Frameworks: {', '.join(analysis.frameworks) if analysis.frameworks else 'None detected'}")
    print(f"  • Structure: {analysis.project_structure}")
    print(f"  • Complexity Score: {analysis.complexity_score}/10")
    print(f"  • Test Coverage: {analysis.test_coverage:.1f}%")

    print(f"\n👥 Team Recommendations:")
    print(f"  • Suggested Team Size: {analysis.suggested_team_size}")
    print(f"  • Suggested Roles:")
    for role in analysis.suggested_roles:
        print(f"    - {role}")

    if analysis.parallelization_opportunities:
        print(f"\n⚡ Parallelization Opportunities:")
        for opp in analysis.parallelization_opportunities:
            print(f"  • {opp}")

    if analysis.risk_areas:
        print(f"\n⚠️  Risk Areas:")
        for risk in analysis.risk_areas:
            print(f"  • {risk}")

    # 生成团队配置建议
    recommendation = generate_team_recommendation(analysis)
    print(f"\n🎯 Team Configuration:")
    print(f"  • Topology: {recommendation['topology']}")
    print(f"  • Methodology: {recommendation['methodology']}")
    print(f"  • Workflow: {' → '.join(recommendation['workflow']['phases'])}")

    # 输出 JSON 格式供其他工具使用
    output_file = Path('project-analysis.json')
    with open(output_file, 'w') as f:
        json.dump(asdict(analysis), f, indent=2)

    print(f"\n✅ Analysis saved to: {output_file}")
    print("=" * 60)

    return analysis

if __name__ == '__main__':
    import sys
    project_path = sys.argv[1] if len(sys.argv) > 1 else '.'
    main(project_path)