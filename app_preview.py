#!/usr/bin/env python3
"""
CostGuard Cloud (AWS) - Interactive Web App Preview Server
Built using pure Python standard library (no external pip dependencies).
"""
import http.server
import socketserver

PORT = 8000

HTML_CONTENT = """<!DOCTYPE html>
<html lang="en" class="dark">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>CostGuard Cloud (AWS) - 60-Second Cloud Waste Audit</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {
                    colors: {
                        brand: { 500: '#ff9900', 600: '#ec8b00', 700: '#cc7700' },
                        darkBg: '#0b1120',
                        cardBg: '#1e293b'
                    }
                }
            }
        }
    </script>
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-darkBg text-slate-100 min-h-screen flex flex-col font-sans antialiased">

    <!-- Top Navigation -->
    <header class="border-b border-slate-800 bg-slate-900/90 backdrop-blur sticky top-0 z-40">
        <div class="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
            <div class="flex items-center space-x-3 cursor-pointer" onclick="window.scrollTo({top:0, behavior:'smooth'})">
                <div class="w-10 h-10 rounded-xl bg-gradient-to-tr from-amber-500 to-orange-600 flex items-center justify-center shadow-lg shadow-orange-500/20">
                    <i class="fa-solid fa-shield-halved text-white text-lg"></i>
                </div>
                <div>
                    <span class="text-xl font-bold bg-gradient-to-r from-white via-slate-200 to-amber-400 bg-clip-text text-transparent">CostGuard Cloud</span>
                    <span class="ml-2 text-xs uppercase px-2 py-0.5 rounded-full bg-amber-500/10 text-amber-400 border border-amber-500/20 font-semibold tracking-wider">AWS Edition</span>
                </div>
            </div>
            <div class="flex items-center space-x-4">
                <button onclick="openHowItWorksModal()" class="text-xs font-semibold px-3 py-1.5 rounded-lg text-slate-300 hover:text-white hover:bg-slate-800 transition flex items-center">
                    <i class="fa-regular fa-circle-question text-amber-400 mr-1.5"></i> How It Works
                </button>
                <span class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                    <span class="w-1.5 h-1.5 rounded-full bg-emerald-400 mr-2 animate-pulse"></span> 100% Read-Only & Safe
                </span>
            </div>
        </div>
    </header>

    <!-- Main Content Area -->
    <main class="max-w-7xl mx-auto px-6 py-10 flex-grow w-full">

        <!-- Hero Section -->
        <div class="text-center max-w-3xl mx-auto mb-10">
            <div class="inline-flex items-center px-3 py-1 rounded-full text-xs font-medium bg-amber-500/10 text-amber-400 border border-amber-500/20 mb-4">
                <i class="fa-solid fa-fire mr-1.5"></i> Built by an AWS Community Builder (Containers)
            </div>
            <h1 class="text-4xl sm:text-5xl font-extrabold tracking-tight text-white mb-4">
                Stop Bleeding Cloud Dollars in <span class="text-amber-400">60 Seconds</span>
            </h1>
            <p class="text-slate-400 text-lg">
                Instantly audit your AWS account for abandoned NAT Gateways, unattached EBS storage, and dangling container images with zero security risk.
            </p>
        </div>

        <!-- Connection Card -->
        <div class="bg-cardBg border border-slate-800 rounded-2xl p-6 sm:p-8 max-w-3xl mx-auto shadow-2xl mb-10">
            <div class="flex items-center justify-between mb-6 border-b border-slate-700/60 pb-4">
                <div>
                    <h2 class="text-lg font-bold text-white flex items-center">
                        <i class="fa-solid fa-key text-amber-400 mr-2.5"></i> Connect AWS Account Safely
                    </h2>
                    <p class="text-xs text-slate-400 mt-1">We never ask for Secret Keys. We use a strictly Read-Only Cross-Account Role.</p>
                </div>
                <button onclick="openHowItWorksModal()" class="text-xs text-amber-400 hover:text-amber-300 transition flex items-center font-medium">
                    How it works <i class="fa-solid fa-arrow-right ml-1.5"></i>
                </button>
            </div>

            <!-- Steps & Form -->
            <div class="space-y-6">
                <!-- Step 1 -->
                <div class="flex items-start space-x-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                    <div class="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm shrink-0 mt-0.5">1</div>
                    <div class="flex-grow">
                        <div class="flex items-center justify-between">
                            <h3 class="text-sm font-semibold text-white">Deploy Read-Only IAM Role</h3>
                            <button onclick="openTemplateModal()" class="text-xs text-amber-400 hover:underline flex items-center">
                                <i class="fa-solid fa-code mr-1"></i> View Template Code
                            </button>
                        </div>
                        <p class="text-xs text-slate-400 mt-0.5">Deploy our verified CloudFormation template. It creates a temporary audit role with 0 write/delete permissions.</p>
                        
                        <div class="flex flex-wrap gap-2.5 mt-3">
                            <button onclick="openTemplateModal()" class="inline-flex items-center text-xs font-semibold px-3 py-1.5 rounded-lg bg-amber-500/10 hover:bg-amber-500/20 text-amber-300 border border-amber-500/30 transition">
                                <i class="fa-solid fa-file-code text-amber-400 mr-2"></i> View CloudFormation YAML
                            </button>
                            <a href="https://console.aws.amazon.com/cloudformation" target="_blank" class="inline-flex items-center text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition">
                                <i class="fa-solid fa-arrow-up-right-from-square text-slate-400 mr-2"></i> Open AWS CloudFormation Console
                            </a>
                        </div>
                    </div>
                </div>

                <!-- Step 2 -->
                <div class="flex items-start space-x-4 bg-slate-900/60 p-4 rounded-xl border border-slate-800">
                    <div class="w-7 h-7 rounded-full bg-amber-500/20 text-amber-400 flex items-center justify-center font-bold text-sm shrink-0 mt-0.5">2</div>
                    <div class="flex-grow">
                        <label for="roleArn" class="block text-sm font-semibold text-white">Paste Generated Role ARN</label>
                        <p class="text-xs text-slate-400 mt-0.5 mb-2">Example: <code class="text-slate-300">arn:aws:iam::123456789012:role/CostGuardCloudAuditRole</code></p>
                        <input type="text" id="roleArn" value="arn:aws:iam::987654321098:role/CostGuardCloudAuditRole" placeholder="arn:aws:iam::..." class="w-full bg-slate-950 border border-slate-700 rounded-lg px-3.5 py-2.5 text-sm text-white focus:outline-none focus:border-amber-400 transition font-mono">
                    </div>
                </div>

                <!-- Launch Button -->
                <button id="scanBtn" onclick="startScan()" class="w-full py-3.5 px-6 rounded-xl bg-gradient-to-r from-amber-500 to-orange-600 hover:from-amber-600 hover:to-orange-700 text-white font-bold text-base shadow-lg shadow-orange-500/25 transition flex items-center justify-center space-x-2">
                    <i class="fa-solid fa-bolt"></i>
                    <span>Run 60-Second Waste Audit</span>
                </button>
            </div>
        </div>

        <!-- Scanner Progress Simulation -->
        <div id="scanningState" class="hidden max-w-3xl mx-auto bg-cardBg border border-slate-800 rounded-2xl p-8 text-center shadow-xl mb-10">
            <div class="inline-block relative w-16 h-16 mb-4">
                <div class="absolute inset-0 border-4 border-amber-500/20 rounded-full"></div>
                <div class="absolute inset-0 border-4 border-amber-500 border-t-transparent rounded-full animate-spin"></div>
            </div>
            <h3 class="text-lg font-bold text-white mb-1" id="scanStatusTitle">Auditing AWS Regions...</h3>
            <p class="text-xs text-slate-400" id="scanStatusSub">Scanning US-East-1 for orphaned resources</p>
            <div class="w-full bg-slate-900 rounded-full h-2 mt-6 overflow-hidden">
                <div id="progressBar" class="bg-gradient-to-r from-amber-500 to-orange-500 h-2 rounded-full transition-all duration-300" style="width: 15%"></div>
            </div>
        </div>

        <!-- Audit Results Dashboard -->
        <div id="resultsDashboard" class="hidden space-y-8 animate-fade-in">

            <!-- Metrics Overview Cards -->
            <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
                <div class="bg-cardBg border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-xl">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-red-500/10 rounded-full blur-2xl"></div>
                    <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Estimated Monthly Waste</span>
                    <div class="text-4xl font-extrabold text-red-400 mt-2 flex items-baseline">
                        <span id="monthlyWaste">$184.20</span>
                        <span class="text-xs text-slate-400 ml-2 font-normal">/ month</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2 flex items-center">
                        <i class="fa-solid fa-arrow-trend-up text-red-400 mr-1.5"></i> Draining your balance continuously
                    </p>
                </div>

                <div class="bg-cardBg border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-xl">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-amber-500/10 rounded-full blur-2xl"></div>
                    <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Projected Annual Leak</span>
                    <div class="text-4xl font-extrabold text-amber-400 mt-2 flex items-baseline">
                        <span id="annualWaste">$2,210.40</span>
                        <span class="text-xs text-slate-400 ml-2 font-normal">/ year</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2 flex items-center">
                        <i class="fa-solid fa-calendar-xmark text-amber-400 mr-1.5"></i> If left unaddressed for 12 months
                    </p>
                </div>

                <div class="bg-cardBg border border-slate-800 p-6 rounded-2xl relative overflow-hidden shadow-xl">
                    <div class="absolute top-0 right-0 w-24 h-24 bg-orange-500/10 rounded-full blur-2xl"></div>
                    <span class="text-xs uppercase font-bold text-slate-400 tracking-wider">Zombie Items Found</span>
                    <div class="text-4xl font-extrabold text-white mt-2 flex items-baseline">
                        <span id="itemsFound">7</span>
                        <span class="text-xs text-slate-400 ml-2 font-normal">resources</span>
                    </div>
                    <p class="text-xs text-slate-400 mt-2 flex items-center">
                        <i class="fa-solid fa-triangle-exclamation text-orange-400 mr-1.5"></i> Across 3 active AWS regions
                    </p>
                </div>
            </div>

            <!-- Findings Table Card -->
            <div class="bg-cardBg border border-slate-800 rounded-2xl shadow-xl overflow-hidden">
                <div class="p-6 border-b border-slate-800 flex items-center justify-between">
                    <div>
                        <h3 class="text-lg font-bold text-white flex items-center">
                            <i class="fa-solid fa-list-check text-amber-400 mr-2.5"></i> Detailed Waste Audit Breakdown
                        </h3>
                        <p class="text-xs text-slate-400 mt-0.5">Exact resource IDs and 1-click remediation commands</p>
                    </div>
                    <button onclick="downloadReport()" class="text-xs font-semibold px-3 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 transition flex items-center">
                        <i class="fa-solid fa-download mr-1.5"></i> Export Report (JSON)
                    </button>
                </div>

                <div class="overflow-x-auto">
                    <table class="w-full text-left border-collapse text-xs">
                        <thead>
                            <tr class="bg-slate-900/60 text-slate-400 border-b border-slate-800 uppercase font-semibold">
                                <th class="p-4">Severity</th>
                                <th class="p-4">Resource Type</th>
                                <th class="p-4">Resource ID & Region</th>
                                <th class="p-4">Details</th>
                                <th class="p-4">Monthly Waste</th>
                                <th class="p-4">Fix Command</th>
                            </tr>
                        </thead>
                        <tbody id="findingsBody" class="divide-y divide-slate-800/60 text-slate-300">
                        </tbody>
                    </table>
                </div>
            </div>

        </div>

    </main>

    <!-- Modal 1: How It Works -->
    <div id="howItWorksModal" class="hidden fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-2xl w-full p-6 sm:p-8 shadow-2xl relative max-h-[90vh] overflow-y-auto">
            <button onclick="closeHowItWorksModal()" class="absolute top-5 right-5 text-slate-400 hover:text-white transition text-lg">
                <i class="fa-solid fa-xmark"></i>
            </button>
            <div class="flex items-center space-x-3 mb-6">
                <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
                    <i class="fa-solid fa-network-wired"></i>
                </div>
                <div>
                    <h2 class="text-xl font-bold text-white">How CostGuard Cloud Works</h2>
                    <p class="text-xs text-slate-400">Security-first, zero-credentials architecture</p>
                </div>
            </div>

            <div class="space-y-4 text-xs text-slate-300">
                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <h4 class="font-bold text-white mb-1 flex items-center text-sm">
                        <span class="w-5 h-5 rounded-full bg-amber-500/20 text-amber-400 inline-flex items-center justify-center text-xs mr-2">1</span>
                        Zero Secret Keys Required
                    </h4>
                    <p class="text-slate-400 leading-relaxed">
                        Traditional tools ask you for your root or IAM secret keys. CostGuard never touches your keys. We use AWS STS Cross-Account IAM roles protected by an External ID.
                    </p>
                </div>

                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <h4 class="font-bold text-white mb-1 flex items-center text-sm">
                        <span class="w-5 h-5 rounded-full bg-amber-500/20 text-amber-400 inline-flex items-center justify-center text-xs mr-2">2</span>
                        Strictly Read-Only Permissions
                    </h4>
                    <p class="text-slate-400 leading-relaxed">
                        The role attaches only AWS managed <code class="text-amber-400">SecurityAudit</code> and Describe policies. Our scanner has zero write permissions and cannot delete, modify, or disrupt any live service.
                    </p>
                </div>

                <div class="bg-slate-950 p-4 rounded-xl border border-slate-800">
                    <h4 class="font-bold text-white mb-1 flex items-center text-sm">
                        <span class="w-5 h-5 rounded-full bg-amber-500/20 text-amber-400 inline-flex items-center justify-center text-xs mr-2">3</span>
                        60-Second Audit & 1-Click Remediation
                    </h4>
                    <p class="text-slate-400 leading-relaxed">
                        The scanner checks active regions for idle NAT Gateways (using 7-day CloudWatch traffic), detached EBS disks, and untagged ECR layers, generating an instant savings estimate and copyable AWS CLI cleanup commands.
                    </p>
                </div>
            </div>

            <div class="mt-6 pt-4 border-t border-slate-800 flex justify-end">
                <button onclick="closeHowItWorksModal()" class="px-4 py-2 rounded-lg bg-amber-500 hover:bg-amber-600 text-white font-semibold text-xs transition">
                    Got It, Let's Scan
                </button>
            </div>
        </div>
    </div>

    <!-- Modal 2: View CloudFormation Template -->
    <div id="templateModal" class="hidden fixed inset-0 z-50 bg-black/75 backdrop-blur-sm flex items-center justify-center p-4">
        <div class="bg-slate-900 border border-slate-800 rounded-2xl max-w-3xl w-full p-6 sm:p-8 shadow-2xl relative max-h-[90vh] flex flex-col">
            <button onclick="closeTemplateModal()" class="absolute top-5 right-5 text-slate-400 hover:text-white transition text-lg">
                <i class="fa-solid fa-xmark"></i>
            </button>
            <div class="flex items-center justify-between mb-4">
                <div class="flex items-center space-x-3">
                    <div class="w-10 h-10 rounded-xl bg-amber-500/20 text-amber-400 flex items-center justify-center text-lg">
                        <i class="fa-solid fa-code"></i>
                    </div>
                    <div>
                        <h2 class="text-lg font-bold text-white">CloudFormation Read-Only Template</h2>
                        <p class="text-xs text-slate-400">Deploy this in your AWS Console to generate your audit role</p>
                    </div>
                </div>
                <button id="copyTemplateBtn" onclick="copyTemplateCode()" class="text-xs font-semibold px-3 py-1.5 rounded-lg bg-slate-800 hover:bg-slate-700 text-amber-400 border border-slate-700 transition flex items-center">
                    <i class="fa-regular fa-copy mr-1.5"></i> Copy YAML
                </button>
            </div>

            <div class="flex-grow overflow-y-auto bg-slate-950 p-4 rounded-xl border border-slate-800 font-mono text-[11px] text-slate-300 leading-relaxed">
<pre id="templateCode">AWSTemplateFormatVersion: '2010-09-09'
Description: 'CostGuard Cloud (AWS) - 1-Click Read-Only Audit Role for Cost & Waste Optimization'

Parameters:
  ExternalId:
    Type: String
    Description: 'Unique External ID provided by CostGuard Cloud'
    Default: 'CostGuardAuditSession'
  CostGuardAccountId:
    Type: String
    Description: 'The AWS Account ID hosting the CostGuard scanner'
    Default: '123456789012'

Resources:
  CostGuardReadOnlyRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: CostGuardCloudAuditRole
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              AWS: !Sub 'arn:aws:iam::${CostGuardAccountId}:root'
            Action: 'sts:AssumeRole'
            Condition:
              StringEquals:
                'sts:ExternalId': !Ref ExternalId
      ManagedPolicyArns:
        # Strictly Read-Only; cannot modify or delete any resources!
        - 'arn:aws:iam::aws:policy/SecurityAudit'
      Policies:
        - PolicyName: CostGuardCostExplorerRead
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - 'ce:GetCostAndUsage'
                  - 'ce:GetDimensionValues'
                  - 'ec2:Describe*'
                  - 'ecr:Describe*'
                  - 'cloudwatch:GetMetricStatistics'
                Resource: '*'

Outputs:
  RoleArn:
    Description: 'Copy this Role ARN and paste it into CostGuard Cloud'
    Value: !GetAtt CostGuardReadOnlyRole.Arn</pre>
            </div>

            <div class="mt-4 pt-3 border-t border-slate-800 flex items-center justify-between">
                <span class="text-xs text-slate-500 font-sans">100% verified Read-Only YAML specification.</span>
                <button onclick="closeTemplateModal()" class="px-4 py-2 rounded-lg bg-slate-800 hover:bg-slate-700 text-white font-semibold text-xs transition">
                    Close
                </button>
            </div>
        </div>
    </div>

    <!-- Footer -->
    <footer class="border-t border-slate-800 bg-slate-900 py-6 text-center text-xs text-slate-500">
        <p>CostGuard Cloud &copy; 2026. Built by an AWS Community Builder (Containers). All rights reserved.</p>
    </footer>

    <script>
        const sampleFindings = [
            {
                severity: "CRITICAL",
                type: "Idle NAT Gateway",
                id: "nat-09f1a234bca889",
                region: "us-east-1",
                details: "VPC vpc-08a1c: Transferred only 0.4 MB in past 7 days",
                waste: "$32.40",
                remediation: "aws ec2 delete-nat-gateway --nat-gateway-id nat-09f1a234bca889 --region us-east-1"
            },
            {
                severity: "CRITICAL",
                type: "Idle NAT Gateway",
                id: "nat-02b4512e09cc99",
                region: "us-west-2",
                details: "VPC vpc-01d7e: 0 active connections recorded",
                waste: "$32.40",
                remediation: "aws ec2 delete-nat-gateway --nat-gateway-id nat-02b4512e09cc99 --region us-west-2"
            },
            {
                severity: "HIGH",
                type: "Unattached EBS Volume",
                id: "vol-0a18e3c12f458e0a",
                region: "us-east-1",
                details: "300 GB (gp3), Status: Available (orphaned 45 days)",
                waste: "$24.00",
                remediation: "aws ec2 delete-volume --volume-id vol-0a18e3c12f458e0a --region us-east-1"
            },
            {
                severity: "HIGH",
                type: "Unattached EBS Volume",
                id: "vol-0fc99e0123778a1b",
                region: "ap-south-1",
                details: "200 GB (gp2), Status: Available (detached from EC2)",
                waste: "$20.00",
                remediation: "aws ec2 delete-volume --volume-id vol-0fc99e0123778a1b --region ap-south-1"
            },
            {
                severity: "MEDIUM",
                type: "Untagged ECR Container Images",
                id: "prod-api-backend",
                region: "us-east-1",
                details: "18 dangling container layers (64.2 GB wasted)",
                waste: "$6.42",
                remediation: "aws ecr put-lifecycle-policy --repository-name prod-api-backend ..."
            },
            {
                severity: "LOW",
                type: "Unassociated Elastic IP",
                id: "3.214.88.19",
                region: "us-east-1",
                details: "Allocated public IP incurring idle hourly fee",
                waste: "$3.60",
                remediation: "aws ec2 release-address --public-ip 3.214.88.19 --region us-east-1"
            },
            {
                severity: "LOW",
                type: "Unassociated Elastic IP",
                id: "54.198.12.77",
                region: "us-west-2",
                details: "Allocated public IP not attached to any ENI",
                waste: "$3.60",
                remediation: "aws ec2 release-address --public-ip 54.198.12.77 --region us-west-2"
            }
        ];

        function openHowItWorksModal() {
            document.getElementById("howItWorksModal").classList.remove("hidden");
        }
        function closeHowItWorksModal() {
            document.getElementById("howItWorksModal").classList.add("hidden");
        }

        function openTemplateModal() {
            document.getElementById("templateModal").classList.remove("hidden");
        }
        function closeTemplateModal() {
            document.getElementById("templateModal").classList.add("hidden");
        }

        function copyTemplateCode() {
            const code = document.getElementById("templateCode").innerText;
            navigator.clipboard.writeText(code).then(() => {
                const btn = document.getElementById("copyTemplateBtn");
                btn.innerHTML = '<i class="fa-solid fa-check mr-1.5 text-emerald-400"></i> Copied!';
                setTimeout(() => {
                    btn.innerHTML = '<i class="fa-regular fa-copy mr-1.5"></i> Copy YAML';
                }, 2000);
            });
        }

        function startScan() {
            const btn = document.getElementById("scanBtn");
            const scanning = document.getElementById("scanningState");
            const results = document.getElementById("resultsDashboard");
            const bar = document.getElementById("progressBar");
            const title = document.getElementById("scanStatusTitle");
            const sub = document.getElementById("scanStatusSub");

            btn.disabled = true;
            btn.classList.add("opacity-50", "cursor-not-allowed");
            scanning.classList.remove("hidden");
            results.classList.add("hidden");

            const stages = [
                { progress: "30%", title: "Querying STS & Cross-Account Role...", sub: "Authenticating session tokens" },
                { progress: "60%", title: "Auditing EC2 & VPC Networks...", sub: "Scanning for idle NAT Gateways & detached EBS" },
                { progress: "85%", title: "Scanning ECR Container Registries...", sub: "Calculating dangling Docker layer storage" },
                { progress: "100%", title: "Finalizing Waste Estimates...", sub: "Applying AWS FinOps cost formulas" }
            ];

            let stageIdx = 0;
            const interval = setInterval(() => {
                if (stageIdx < stages.length) {
                    bar.style.width = stages[stageIdx].progress;
                    title.innerText = stages[stageIdx].title;
                    sub.innerText = stages[stageIdx].sub;
                    stageIdx++;
                } else {
                    clearInterval(interval);
                    renderResults();
                }
            }, 700);
        }

        function renderResults() {
            document.getElementById("scanningState").classList.add("hidden");
            document.getElementById("resultsDashboard").classList.remove("hidden");
            document.getElementById("scanBtn").disabled = false;
            document.getElementById("scanBtn").classList.remove("opacity-50", "cursor-not-allowed");

            const tbody = document.getElementById("findingsBody");
            tbody.innerHTML = "";

            sampleFindings.forEach(item => {
                const tr = document.createElement("tr");
                tr.className = "hover:bg-slate-800/40 transition";

                let badgeColor = "bg-slate-700 text-slate-300";
                if (item.severity === "CRITICAL") badgeColor = "bg-red-500/10 text-red-400 border border-red-500/20";
                if (item.severity === "HIGH") badgeColor = "bg-orange-500/10 text-orange-400 border border-orange-500/20";
                if (item.severity === "MEDIUM") badgeColor = "bg-amber-500/10 text-amber-400 border border-amber-500/20";
                if (item.severity === "LOW") badgeColor = "bg-blue-500/10 text-blue-400 border border-blue-500/20";

                tr.innerHTML = `
                    <td class="p-4"><span class="px-2 py-0.5 rounded text-[10px] font-bold ${badgeColor}">${item.severity}</span></td>
                    <td class="p-4 font-semibold text-white">${item.type}</td>
                    <td class="p-4 font-mono text-slate-300"><span class="text-amber-400 font-bold">${item.region}</span>: ${item.id}</td>
                    <td class="p-4 text-slate-400">${item.details}</td>
                    <td class="p-4 font-bold text-red-400">${item.waste} / mo</td>
                    <td class="p-4">
                        <button onclick="navigator.clipboard.writeText('${item.remediation.replace(/'/g, "\\\'")}'); alert('Copied fix command to clipboard!');" class="px-2.5 py-1 rounded bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700 text-[11px] font-mono transition">
                            <i class="fa-regular fa-copy mr-1 text-amber-400"></i> Copy CLI Fix
                        </button>
                    </td>
                `;
                tbody.appendChild(tr);
            });

            document.getElementById("resultsDashboard").scrollIntoView({ behavior: 'smooth' });
        }

        function downloadReport() {
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(sampleFindings, null, 2));
            const dlAnchor = document.createElement('a');
            dlAnchor.setAttribute("href", dataStr);
            dlAnchor.setAttribute("download", "CostGuard_Cloud_Audit_Report.json");
            dlAnchor.click();
        }
    </script>
</body>
</html>
"""


class WebAppHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(HTML_CONTENT.encode("utf-8"))


if __name__ == "__main__":
    with socketserver.TCPServer(("0.0.0.0", PORT), WebAppHandler) as httpd:
        print(f"🚀 CostGuard Cloud (AWS) Web App running live on http://localhost:{PORT}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")
