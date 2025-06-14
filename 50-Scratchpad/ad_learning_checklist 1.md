# HTB Active Directory Attack Checklist

## Easy Difficulty
- [ ] **Active** - Kerberoasting + GPP password attacks
- [ ] **Forest** - AS-REP Roasting + DCSync + Exchange permissions
- [ ] **Sauna** - AS-REP Roasting + AutoLogon credentials + DCSync

## Medium Difficulty  
- [ ] **Resolute** - Password spraying + DnsAdmins exploitation
- [ ] **Cascade** - LDAP enumeration + AD Recycle Bin abuse
- [ ] **Intelligence** - Constrained delegation + gMSA + DNS poisoning
- [ ] **Monteverde** - Azure AD Connect exploitation
- [ ] **Fuse** - Password spraying + print spooler abuse
- [ ] **Authority** - ADCS exploitation (ESC1)
- [ ] **Certified** - Advanced ADCS + Shadow Credentials
- [ ] **Vintage** - Pre-2000 compatibility + GMSA abuse
- [ ] **Adagio** - AS-REP Roasting + RBCD attacks
- [ ] **Outdated** - ADCS + Shadow Credentials
- [ ] **Manager** - SMB enumeration + credential discovery

## Hard Difficulty
- [ ] **Blackfield** - AS-REP Roasting + LSASS analysis + Backup Operators
- [ ] **Search** - Certificate attacks + GMSA + PowerShell Web Access
- [ ] **Object** - BloodHound + GenericWrite abuse
- [ ] **Multimaster** - SQL injection in AD + Certificate Services
- [ ] **Freelancer** - MSSQL impersonation + RBCD + memory dumps
- [ ] **Rebound** - RID cycling + cross-session relay + GMSA abuse

## Insane Difficulty
- [ ] **Sizzle** - Advanced certificate attacks + multi-domain
- [ ] **PivotAPI** - Multi-hop attacks + MSSQL + complex tunneling
- [ ] **Acute** - PowerShell constraint bypass + advanced lateral movement

## Key Attack Techniques Covered
- Kerberoasting & AS-REP Roasting
- DCSync attacks
- Certificate Services exploitation
- Delegation attacks (Constrained, RBCD)
- Golden/Silver Tickets
- BloodHound attack path analysis
- Memory dump analysis
- Cross-domain trust exploitation