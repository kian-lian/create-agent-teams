#!/usr/bin/env python3
"""
Team Validation Script for Agent Teams
验证团队配置的有效性和优化建议
"""

import json
import yaml
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple, Any
from dataclasses import dataclass
from enum import Enum

class ValidationLevel(Enum):
    """验证级别"""
    ERROR = "error"      # 必须修复
    WARNING = "warning"  # 建议修复
    INFO = "info"       # 信息提示

@dataclass
class ValidationIssue:
    """验证问题"""
    level: ValidationLevel
    category: str
    message: str
    suggestion: Optional[str] = None
    path: Optional[str] = None

class TeamValidator:
    """团队配置验证器"""

    def __init__(self, config_path: str):
        """初始化验证器"""
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.issues: List[ValidationIssue] = []
        self.role_models = {
            'ceo': 'opus',
            'cto': 'opus',
            'product-owner': 'opus',
            'tech-lead': 'opus',
            'architect': 'sonnet',
            'developer': 'sonnet',
            'designer': 'sonnet',
            'qa': 'sonnet',
            'writer': 'haiku',
            'monitor': 'haiku'
        }

    def _load_config(self) -> Dict:
        """加载团队配置"""
        if self.config_path.suffix == '.yaml':
            with open(self.config_path) as f:
                return yaml.safe_load(f)
        elif self.config_path.suffix == '.json':
            with open(self.config_path) as f:
                return json.load(f)
        else:
            raise ValueError(f"Unsupported config format: {self.config_path.suffix}")

    def validate(self) -> Tuple[bool, List[ValidationIssue]]:
        """执行完整验证"""
        self.issues = []

        # 运行所有验证检查
        self._validate_structure()
        self._validate_roles()
        self._validate_workflow()
        self._validate_communication()
        self._validate_dependencies()
        self._validate_resources()
        self._validate_best_practices()

        # 返回是否有错误
        has_errors = any(issue.level == ValidationLevel.ERROR for issue in self.issues)
        return not has_errors, self.issues

    def _add_issue(self, level: ValidationLevel, category: str, message: str,
                   suggestion: Optional[str] = None, path: Optional[str] = None):
        """添加验证问题"""
        self.issues.append(ValidationIssue(level, category, message, suggestion, path))

    def _validate_structure(self):
        """验证配置结构"""
        required_fields = ['name', 'roles', 'workflow']

        for field in required_fields:
            if field not in self.config:
                self._add_issue(
                    ValidationLevel.ERROR,
                    'structure',
                    f"Missing required field: {field}",
                    f"Add '{field}' to your configuration",
                    field
                )

        # 检查团队名称
        if 'name' in self.config:
            name = self.config['name']
            if not name or not isinstance(name, str):
                self._add_issue(
                    ValidationLevel.ERROR,
                    'structure',
                    "Team name must be a non-empty string",
                    "Provide a descriptive team name"
                )

    def _validate_roles(self):
        """验证角色配置"""
        if 'roles' not in self.config:
            return

        roles = self.config['roles']

        if not roles:
            self._add_issue(
                ValidationLevel.ERROR,
                'roles',
                "Team must have at least one role",
                "Add role definitions to your team"
            )
            return

        # 检查每个角色
        role_ids = set()
        for i, role in enumerate(roles):
            role_path = f"roles[{i}]"

            # 检查必需字段
            if 'id' not in role:
                self._add_issue(
                    ValidationLevel.ERROR,
                    'roles',
                    f"Role at index {i} missing 'id' field",
                    "Add unique identifier for the role",
                    role_path
                )
            else:
                # 检查ID唯一性
                if role['id'] in role_ids:
                    self._add_issue(
                        ValidationLevel.ERROR,
                        'roles',
                        f"Duplicate role ID: {role['id']}",
                        "Ensure all role IDs are unique",
                        role_path
                    )
                role_ids.add(role['id'])

            # 检查模型配置
            if 'model' in role:
                model = role['model']
                if model not in ['opus', 'sonnet', 'haiku']:
                    self._add_issue(
                        ValidationLevel.ERROR,
                        'roles',
                        f"Invalid model '{model}' for role {role.get('id', i)}",
                        "Use one of: opus, sonnet, haiku",
                        f"{role_path}.model"
                    )

                # 模型优化建议
                role_type = role.get('type', '')
                suggested_model = self._suggest_model(role_type)
                if suggested_model and model != suggested_model:
                    self._add_issue(
                        ValidationLevel.INFO,
                        'optimization',
                        f"Role '{role.get('id')}' uses {model}, but {suggested_model} might be more cost-effective",
                        f"Consider using {suggested_model} for {role_type} roles",
                        f"{role_path}.model"
                    )

            # 检查职责定义
            if 'responsibilities' not in role or not role['responsibilities']:
                self._add_issue(
                    ValidationLevel.WARNING,
                    'roles',
                    f"Role '{role.get('id')}' has no defined responsibilities",
                    "Add clear responsibilities for better task allocation",
                    f"{role_path}.responsibilities"
                )

        # 团队规模检查
        team_size = len(roles)
        if team_size > 15:
            self._add_issue(
                ValidationLevel.WARNING,
                'roles',
                f"Large team size ({team_size}) may cause coordination overhead",
                "Consider splitting into smaller sub-teams",
                "roles"
            )
        elif team_size < 3:
            self._add_issue(
                ValidationLevel.INFO,
                'roles',
                f"Small team size ({team_size}) may limit parallelization",
                "Consider if additional roles would help",
                "roles"
            )

    def _suggest_model(self, role_type: str) -> Optional[str]:
        """建议最优模型"""
        for key, model in self.role_models.items():
            if key in role_type.lower():
                return model
        return 'sonnet'  # 默认建议

    def _validate_workflow(self):
        """验证工作流配置"""
        if 'workflow' not in self.config:
            return

        workflow = self.config['workflow']

        if 'phases' not in workflow:
            self._add_issue(
                ValidationLevel.WARNING,
                'workflow',
                "No workflow phases defined",
                "Define phases for better task organization",
                "workflow.phases"
            )
            return

        phases = workflow['phases']
        phase_names = set()
        total_duration = 0

        for i, phase in enumerate(phases):
            phase_path = f"workflow.phases[{i}]"

            # 检查必需字段
            if 'name' not in phase:
                self._add_issue(
                    ValidationLevel.ERROR,
                    'workflow',
                    f"Phase at index {i} missing 'name'",
                    "Add name for the phase",
                    phase_path
                )
            else:
                # 检查重复
                if phase['name'] in phase_names:
                    self._add_issue(
                        ValidationLevel.ERROR,
                        'workflow',
                        f"Duplicate phase name: {phase['name']}",
                        "Ensure phase names are unique",
                        f"{phase_path}.name"
                    )
                phase_names.add(phase['name'])

            # 检查依赖
            if 'dependencies' in phase:
                for dep in phase['dependencies']:
                    if dep not in phase_names:
                        self._add_issue(
                            ValidationLevel.ERROR,
                            'workflow',
                            f"Phase '{phase.get('name')}' depends on undefined phase '{dep}'",
                            f"Ensure '{dep}' is defined before this phase",
                            f"{phase_path}.dependencies"
                        )

            # 检查持续时间
            if 'duration' in phase:
                duration = phase['duration']
                if isinstance(duration, str) and duration.endswith('%'):
                    try:
                        total_duration += int(duration[:-1])
                    except ValueError:
                        pass

        # 检查总持续时间
        if total_duration > 0 and total_duration != 100:
            self._add_issue(
                ValidationLevel.WARNING,
                'workflow',
                f"Phase durations sum to {total_duration}%, not 100%",
                "Adjust phase durations to sum to 100%",
                "workflow.phases"
            )

    def _validate_communication(self):
        """验证通信配置"""
        if 'communication' not in self.config:
            self._add_issue(
                ValidationLevel.INFO,
                'communication',
                "No communication protocols defined",
                "Consider defining communication channels and protocols"
            )
            return

        comm = self.config['communication']

        if 'channels' in comm:
            channels = comm['channels']

            # 检查是否有同步通信
            has_sync = any(ch.get('type') == 'synchronous' for ch in channels)
            if not has_sync:
                self._add_issue(
                    ValidationLevel.WARNING,
                    'communication',
                    "No synchronous communication channel defined",
                    "Add at least one synchronous channel (e.g., daily standup)"
                )

            # 检查通信频率
            for i, channel in enumerate(channels):
                if 'frequency' not in channel:
                    self._add_issue(
                        ValidationLevel.INFO,
                        'communication',
                        f"Channel '{channel.get('name', i)}' has no defined frequency",
                        "Specify communication frequency",
                        f"communication.channels[{i}].frequency"
                    )

    def _validate_dependencies(self):
        """验证依赖关系"""
        if 'roles' not in self.config:
            return

        roles = self.config['roles']
        role_ids = {role['id'] for role in roles if 'id' in role}

        # 检查报告关系
        for role in roles:
            if 'reports_to' in role:
                supervisor = role['reports_to']
                if supervisor not in role_ids:
                    self._add_issue(
                        ValidationLevel.ERROR,
                        'dependencies',
                        f"Role '{role['id']}' reports to undefined role '{supervisor}'",
                        f"Ensure '{supervisor}' is defined in roles",
                        f"roles.{role['id']}.reports_to"
                    )

        # 检查循环依赖
        def has_cycle(graph: Dict[str, str]) -> bool:
            visited = set()
            rec_stack = set()

            def visit(node):
                if node in rec_stack:
                    return True
                if node in visited:
                    return False

                visited.add(node)
                rec_stack.add(node)

                if node in graph:
                    if visit(graph[node]):
                        return True

                rec_stack.remove(node)
                return False

            for node in graph:
                if node not in visited:
                    if visit(node):
                        return True
            return False

        reporting = {role['id']: role['reports_to']
                    for role in roles
                    if 'id' in role and 'reports_to' in role}

        if has_cycle(reporting):
            self._add_issue(
                ValidationLevel.ERROR,
                'dependencies',
                "Circular reporting dependency detected",
                "Remove circular dependencies in reporting structure"
            )

    def _validate_resources(self):
        """验证资源配置"""
        if 'token_budget' in self.config:
            budget = self.config['token_budget']
            if budget not in ['premium', 'balanced', 'economic']:
                self._add_issue(
                    ValidationLevel.WARNING,
                    'resources',
                    f"Unknown token budget '{budget}'",
                    "Use one of: premium, balanced, economic",
                    "token_budget"
                )

        # 检查模型使用与预算匹配
        if 'roles' in self.config and 'token_budget' in self.config:
            budget = self.config['token_budget']
            roles = self.config['roles']

            opus_count = sum(1 for r in roles if r.get('model') == 'opus')
            total_count = len(roles)

            if budget == 'economic' and opus_count > 1:
                self._add_issue(
                    ValidationLevel.WARNING,
                    'resources',
                    f"Economic budget with {opus_count} Opus agents may be expensive",
                    "Consider using more Sonnet/Haiku models",
                    "roles"
                )
            elif budget == 'premium' and opus_count < 2:
                self._add_issue(
                    ValidationLevel.INFO,
                    'resources',
                    "Premium budget allows for more Opus agents if needed",
                    "Consider using Opus for critical decision-making roles"
                )

    def _validate_best_practices(self):
        """验证最佳实践"""
        # 检查是否有质量门控
        if 'quality_gates' not in self.config:
            self._add_issue(
                ValidationLevel.INFO,
                'best-practices',
                "No quality gates defined",
                "Consider adding quality checkpoints"
            )

        # 检查错误恢复策略
        if 'error_recovery' not in self.config:
            self._add_issue(
                ValidationLevel.WARNING,
                'best-practices',
                "No error recovery strategy defined",
                "Add error recovery mechanisms for resilience"
            )

        # 检查成功指标
        if 'success_metrics' not in self.config:
            self._add_issue(
                ValidationLevel.INFO,
                'best-practices',
                "No success metrics defined",
                "Define measurable success criteria"
            )

        # 检查并行化机会
        if 'workflow' in self.config and 'phases' in self.config['workflow']:
            phases = self.config['workflow']['phases']
            has_parallel = any('parallel' in str(phase) for phase in phases)

            if not has_parallel and len(phases) > 3:
                self._add_issue(
                    ValidationLevel.INFO,
                    'optimization',
                    "No parallel phases detected in workflow",
                    "Consider parallelizing independent tasks for faster completion"
                )

def generate_optimization_report(issues: List[ValidationIssue]) -> str:
    """生成优化报告"""
    report = []
    report.append("\n" + "="*60)
    report.append("TEAM CONFIGURATION VALIDATION REPORT")
    report.append("="*60 + "\n")

    # 按级别分组
    errors = [i for i in issues if i.level == ValidationLevel.ERROR]
    warnings = [i for i in issues if i.level == ValidationLevel.WARNING]
    info = [i for i in issues if i.level == ValidationLevel.INFO]

    # 摘要
    report.append("📊 Summary:")
    report.append(f"  • Errors: {len(errors)}")
    report.append(f"  • Warnings: {len(warnings)}")
    report.append(f"  • Info: {len(info)}")
    report.append("")

    # 错误
    if errors:
        report.append("❌ ERRORS (must fix):")
        for issue in errors:
            report.append(f"\n  [{issue.category}] {issue.message}")
            if issue.suggestion:
                report.append(f"    💡 {issue.suggestion}")
            if issue.path:
                report.append(f"    📍 Location: {issue.path}")

    # 警告
    if warnings:
        report.append("\n⚠️  WARNINGS (should fix):")
        for issue in warnings:
            report.append(f"\n  [{issue.category}] {issue.message}")
            if issue.suggestion:
                report.append(f"    💡 {issue.suggestion}")
            if issue.path:
                report.append(f"    📍 Location: {issue.path}")

    # 信息
    if info:
        report.append("\nℹ️  INFO (suggestions):")
        for issue in info:
            report.append(f"\n  [{issue.category}] {issue.message}")
            if issue.suggestion:
                report.append(f"    💡 {issue.suggestion}")

    # 结论
    report.append("\n" + "-"*60)
    if errors:
        report.append("❌ Validation FAILED - Please fix errors before proceeding")
    elif warnings:
        report.append("⚠️  Validation PASSED with warnings - Consider addressing warnings")
    else:
        report.append("✅ Validation PASSED - Configuration is ready to use")

    return "\n".join(report)

def main(config_path: str):
    """主函数"""
    print(f"\n🔍 Validating team configuration: {config_path}")

    try:
        validator = TeamValidator(config_path)
        valid, issues = validator.validate()

        # 生成报告
        report = generate_optimization_report(issues)
        print(report)

        # 保存详细结果
        output_file = Path('validation-report.json')
        with open(output_file, 'w') as f:
            json.dump([{
                'level': issue.level.value,
                'category': issue.category,
                'message': issue.message,
                'suggestion': issue.suggestion,
                'path': issue.path
            } for issue in issues], f, indent=2)

        print(f"\n💾 Detailed report saved to: {output_file}")

        # 返回状态码
        return 0 if valid else 1

    except Exception as e:
        print(f"\n❌ Validation failed: {e}")
        return 2

if __name__ == '__main__':
    import sys
    if len(sys.argv) < 2:
        print("Usage: python validate_team.py <config_file>")
        sys.exit(1)

    config_file = sys.argv[1]
    exit_code = main(config_file)
    sys.exit(exit_code)