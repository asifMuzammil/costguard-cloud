from typing import List, Dict, Any


def generate_text_report(scan_results: List[Dict[str, Any]], account_id: str, regions_scanned: List[str]) -> str:
    """
    Generates a clean terminal text summary.
    """
    total_waste = sum(item["monthly_waste_usd"] for item in scan_results)
    annual_waste = total_waste * 12

    lines = []
    lines.append("=" * 70)
    lines.append(f"  CostGuard Cloud (AWS) - Waste Audit Report")
    lines.append(f"  Target Account: {account_id}")
    lines.append(f"  Regions Scanned: {', '.join(regions_scanned)}")
    lines.append("=" * 70)
    lines.append("")
    lines.append(f"💰 ESTIMATED MONTHLY WASTE : ${total_waste:,.2f} USD")
    lines.append(f"📉 PROJECTED ANNUAL LEAK    : ${annual_waste:,.2f} USD")
    lines.append(f"🔍 TOTAL ZOMBIE ITEMS FOUND : {len(scan_results)}")
    lines.append("")
    lines.append("-" * 70)

    if not scan_results:
        lines.append("🎉 Clean bill of health! No common zombie resources detected.")
    else:
        for idx, item in enumerate(scan_results, 1):
            severity = item.get("severity", "MEDIUM")
            lines.append(f"[{idx}] [{severity}] {item['resource_type']}")
            lines.append(f"    ID     : {item['resource_id']} ({item.get('name', 'Unnamed')})")
            lines.append(f"    Region : {item['region']}")
            lines.append(f"    Details: {item['details']}")
            lines.append(f"    Waste  : ${item['monthly_waste_usd']:,.2f} / month")
            lines.append(f"    Fix    : {item['remediation_cli']}")
            lines.append("")

    lines.append("=" * 70)
    return "\n".join(lines)


def generate_json_report(scan_results: List[Dict[str, Any]], account_id: str, regions_scanned: List[str]) -> Dict[str, Any]:
    total_waste = sum(item["monthly_waste_usd"] for item in scan_results)
    return {
        "status": "success",
        "account_id": account_id,
        "regions_scanned": regions_scanned,
        "total_zombie_resources": len(scan_results),
        "estimated_monthly_waste_usd": round(total_waste, 2),
        "estimated_annual_waste_usd": round(total_waste * 12, 2),
        "findings": scan_results
    }


def generate_html_report(scan_results: List[Dict[str, Any]], account_id: str, regions_scanned: List[str]) -> str:
    """
    Generates a standalone, beautiful Dark-Mode HTML report with Tailwind styling.
    """
    total_waste = sum(item["monthly_waste_usd"] for item in scan_results)
    annual_waste = total_waste * 12
    item_count = len(scan_results)

    # Group findings by resource_type
    grouped: Dict[str, List[Dict[str, Any]]] = {}
    for item in scan_results:
        rtype = item.get("resource_type", "Other")
        grouped.setdefault(rtype, []).append(item)

    # Build rows HTML
    rows_html = ""
    if not scan_results:
        rows_html = """
        <div class="p-8 text-center bg-slate-800/40 rounded-2xl border border-emerald-500/20">
            <div class="inline-flex p-3 rounded-full bg-emerald-500/10 text-emerald-400 mb-3 text-2xl">🎉</div>
            <h3 class="text-xl font-bold text-white mb-1">Clean Bill of Health!</h3>
            <p class="text-slate-400 text-sm">No common zombie resources or unattached assets detected in the scanned regions.</p>
        </div>
        """
    else:
        for idx, item in enumerate(scan_results, 1):
            severity = item.get("severity", "MEDIUM")
            badge_color = "bg-rose-500/20 text-rose-400 border-rose-500/30" if severity == "CRITICAL" else \
                          "bg-amber-500/20 text-amber-400 border-amber-500/30" if severity == "HIGH" else \
                          "bg-blue-500/20 text-blue-400 border-blue-500/30"
            
            fix_cli = item.get("remediation_cli", "").replace('"', '&quot;')
            rows_html += f"""
            <div class="bg-slate-800/60 border border-slate-700/60 rounded-xl p-5 hover:border-slate-600 transition-all">
                <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-3 mb-3">
                    <div class="flex items-center gap-3">
                        <span class="px-2.5 py-1 text-xs font-semibold rounded-md border {badge_color}">{severity}</span>
                        <h4 class="text-base font-semibold text-white">{item['resource_type']}</h4>
                    </div>
                    <div class="text-right">
                        <span class="text-lg font-bold text-rose-400">${item['monthly_waste_usd']:,.2f}</span>
                        <span class="text-xs text-slate-400"> / month</span>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 sm:grid-cols-3 gap-2 text-xs text-slate-300 mb-4 bg-slate-900/40 p-3 rounded-lg border border-slate-800">
                    <div><span class="text-slate-500">Resource ID:</span> <span class="font-mono text-slate-200">{item['resource_id']}</span></div>
                    <div><span class="text-slate-500">Region:</span> <span class="text-slate-200 font-medium">{item['region']}</span></div>
                    <div><span class="text-slate-500">Details:</span> <span class="text-slate-200">{item['details']}</span></div>
                </div>

                <div class="flex items-center justify-between gap-3 bg-slate-950 p-3 rounded-lg border border-slate-800 text-xs font-mono">
                    <span class="text-slate-400 truncate select-all">{item.get('remediation_cli', '')}</span>
                    <button onclick="navigator.clipboard.writeText('{fix_cli}'); this.innerText='Copied!'; setTimeout(()=>this.innerText='Copy Fix', 2000)" 
                            class="shrink-0 px-3 py-1 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded text-xs transition-colors border border-slate-700">
                        Copy Fix
                    </button>
                </div>
            </div>
            """

    regions_str = ", ".join(regions_scanned)
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CostGuard Cloud Audit Report - {account_id}</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
    <style>
        body {{ font-family: 'Inter', sans-serif; }}
        code, pre, .font-mono {{ font-family: 'JetBrains Mono', monospace; }}
    </style>
</head>
<body class="bg-slate-950 text-slate-100 min-h-screen py-10 px-4 sm:px-8">
    <div class="max-w-5xl mx-auto space-y-8">
        
        <!-- Header -->
        <div class="flex flex-col sm:flex-row sm:items-center justify-between pb-6 border-b border-slate-800 gap-4">
            <div class="flex items-center gap-3">
                <div class="p-2.5 rounded-xl bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 text-2xl">
                    🛡️
                </div>
                <div>
                    <h1 class="text-2xl font-bold tracking-tight text-white">CostGuard Cloud (AWS)</h1>
                    <p class="text-xs text-slate-400">Zero-Knowledge Zombie Resource & Waste Audit</p>
                </div>
            </div>
            <div class="flex items-center gap-3">
                <span class="px-3 py-1 text-xs rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 flex items-center gap-1.5 font-medium">
                    <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> 100% Read-Only Audit
                </span>
                <button onclick="window.print()" class="px-3 py-1.5 bg-slate-800 hover:bg-slate-700 text-slate-200 rounded-lg text-xs font-medium border border-slate-700 transition-colors">
                    🖨️ Export / Print PDF
                </button>
            </div>
        </div>

        <!-- Meta Information Banner -->
        <div class="grid grid-cols-2 sm:grid-cols-4 gap-4 p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs">
            <div>
                <span class="text-slate-500 block">Target Account</span>
                <span class="font-mono text-slate-200 font-semibold">{account_id}</span>
            </div>
            <div>
                <span class="text-slate-500 block">Scanned Regions</span>
                <span class="text-slate-200 font-semibold truncate block" title="{regions_str}">{regions_str}</span>
            </div>
            <div>
                <span class="text-slate-500 block">Security Audit Mode</span>
                <span class="text-emerald-400 font-medium">Strictly Read-Only (:ro)</span>
            </div>
            <div>
                <span class="text-slate-500 block">Audit Engine</span>
                <span class="text-slate-200 font-medium">CostGuard CLI v1.0.0</span>
            </div>
        </div>

        <!-- Summary Metric Cards -->
        <div class="grid grid-cols-1 sm:grid-cols-3 gap-5">
            <div class="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-900/60 border border-rose-500/20 relative overflow-hidden">
                <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-rose-500/5 rounded-full blur-2xl pointer-events-none"></div>
                <span class="text-xs font-semibold text-rose-400 tracking-wider uppercase">Monthly Waste Detected</span>
                <div class="text-3xl font-extrabold text-white mt-2">${total_waste:,.2f} <span class="text-sm font-normal text-slate-400">/ mo</span></div>
                <p class="text-xs text-slate-500 mt-2">Identified in idle or unattached resources</p>
            </div>

            <div class="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-900/60 border border-amber-500/20 relative overflow-hidden">
                <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-amber-500/5 rounded-full blur-2xl pointer-events-none"></div>
                <span class="text-xs font-semibold text-amber-400 tracking-wider uppercase">Projected Annual Leak</span>
                <div class="text-3xl font-extrabold text-white mt-2">${annual_waste:,.2f} <span class="text-sm font-normal text-slate-400">/ yr</span></div>
                <p class="text-xs text-slate-500 mt-2">Compounded 12-month drain without remediation</p>
            </div>

            <div class="p-6 rounded-2xl bg-gradient-to-b from-slate-900 to-slate-900/60 border border-emerald-500/20 relative overflow-hidden">
                <div class="absolute -right-4 -bottom-4 w-24 h-24 bg-emerald-500/5 rounded-full blur-2xl pointer-events-none"></div>
                <span class="text-xs font-semibold text-emerald-400 tracking-wider uppercase">Zombie Assets Found</span>
                <div class="text-3xl font-extrabold text-white mt-2">{item_count} <span class="text-sm font-normal text-slate-400">assets</span></div>
                <p class="text-xs text-slate-500 mt-2">Detached volumes, idle NATs & unused IPs</p>
            </div>
        </div>

        <!-- Findings List -->
        <div class="space-y-4">
            <div class="flex items-center justify-between">
                <h3 class="text-lg font-bold text-white flex items-center gap-2">
                    <span>Identified Waste Assets</span>
                    <span class="px-2 py-0.5 text-xs rounded-full bg-slate-800 text-slate-400 border border-slate-700">{item_count}</span>
                </h3>
                <span class="text-xs text-slate-500">Copy commands to remediate safely in your terminal</span>
            </div>
            
            <div class="space-y-3">
                {rows_html}
            </div>
        </div>

        <!-- Footer / Security Note -->
        <div class="pt-8 border-t border-slate-900 text-center text-xs text-slate-500 space-y-2">
            <p>🛡️ CostGuard Cloud does not delete or modify your infrastructure. All remediations are suggested for review.</p>
            <p class="text-slate-600">Built for the AWS Community by <span class="text-slate-400 font-medium">Asif Muzammil</span> (AWS Community Builder). Open-source & zero-telemetry.</p>
        </div>

    </div>
</body>
</html>"""
