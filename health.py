"""Auditoria rápida e sem dependências para repositórios de software."""
import argparse
import json
from pathlib import Path

RULES = {
    "README": (lambda p: any(p.glob("README*")), "Adicione um README com instalação e exemplos."),
    "LICENSE": (lambda p: any(p.glob("LICENSE*")), "Defina uma licença para uso e contribuição."),
    "Gitignore": (lambda p: (p / ".gitignore").exists(), "Evite publicar caches, builds e segredos."),
    "CI": (lambda p: (p / ".github/workflows").exists(), "Automatize testes em .github/workflows."),
    "Testes": (lambda p: any((p / x).exists() for x in ("tests", "test", "__tests__")), "Crie uma suíte de testes reproduzível."),
    "Segurança": (lambda p: any((p / x).exists() for x in ("SECURITY.md", ".github/SECURITY.md")), "Documente como reportar vulnerabilidades."),
    "Contribuição": (lambda p: any((p / x).exists() for x in ("CONTRIBUTING.md", ".github/CONTRIBUTING.md")), "Explique como contribuir."),
}


def scan(path):
    project = Path(path)
    checks = {name: bool(test(project)) for name, (test, _hint) in RULES.items()}
    score = round(sum(checks.values()) / len(checks) * 100)
    suggestions = [hint for name, (_test, hint) in RULES.items() if not checks[name]]
    level = "excelente" if score >= 85 else "bom" if score >= 65 else "em evolução" if score >= 40 else "inicial"
    return {"project": project.name, "score": score, "level": level, "checks": checks, "suggestions": suggestions}


def main(argv=None):
    parser = argparse.ArgumentParser(description="Avalie a saúde de um repositório")
    parser.add_argument("path", nargs="?", default=".")
    parser.add_argument("--json", action="store_true")
    parser.add_argument("--minimum", type=int, default=0, help="falha se a nota ficar abaixo deste valor")
    args = parser.parse_args(argv)
    result = scan(args.path)
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        print(f"AgentOS Project Health · {result['project']} · {result['score']}/100 · {result['level']}")
        for name, ok in result["checks"].items():
            print(f"{'OK' if ok else '--'} {name}")
        if result["suggestions"]:
            print("\nPróximas melhorias:")
            for suggestion in result["suggestions"]:
                print(f"- {suggestion}")
    return 0 if result["score"] >= args.minimum else 1


if __name__ == "__main__":
    raise SystemExit(main())
