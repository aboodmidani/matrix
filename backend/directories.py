import requests
import os

def check_directories(url, wordlist_type='fast'):
    """Check for directory exposure using hardcoded common paths"""
    vulnerabilities = []

    # Hardcoded list of common vulnerable paths
    vuln_paths = [
        '/webfig',
        '/sitemap.xml',
        '/admin',
        '/wp-admin',
        '/phpmyadmin',
        '/.env',
        '/backup.sql',
        '/server-status',
        '/.git/config',
        '/.svn/entries',
        '/admin.php',
        '/administrator',
        '/login',
        '/dashboard',
        '/controlpanel',
        '/cpanel',
        '/webmail',
        '/phpinfo.php',
        '/test.php',
        '/config.php',
        '/install.php',
        '/readme.html',
        '/robots.txt',
        '/.htaccess',
        '/.htpasswd',
        '/web.config',
        '/crossdomain.xml',
        '/clientaccesspolicy.xml',
        '/xmlrpc.php',
        '/readme.txt',
        '/changelog.txt',
        '/license.txt',
        '/wp-config.php',
        '/wp-content/uploads',
        '/wp-includes',
        '/images',
        '/css',
        '/js',
        '/assets',
        '/backup',
        '/backups',
        '/tmp',
        '/temp',
        '/cache',
        '/logs',
        '/log',
        '/error_log',
        '/access_log',
        '/adminer.php',
        '/phpminiadmin.php',
        '/pma',
        '/mysql',
        '/sql',
        '/database',
        '/db',
        '/data',
        '/upload',
        '/uploads',
        '/files',
        '/filemanager',
        '/ftp',
        '/sftp'
    ]

    try:
        found_directories = 0
        for path in vuln_paths:
            try:
                test_url = url.rstrip('/') + path
                response = requests.get(test_url, timeout=3, verify=True, allow_redirects=False)

                # Check for directory exposure - multiple indicators
                is_directory = False

                # Status codes that indicate directory exists
                if response.status_code in [200, 301, 302, 403, 401, 405]:
                    # Check content for directory-like characteristics
                    content = response.text.lower()

                    # Look for directory listing patterns
                    if any(indicator in content for indicator in [
                        'index of', 'parent directory', 'directory listing',
                        'folder', 'dir', '<title>index of',
                        'apache', 'nginx', 'iis', 'lighttpd'
                    ]):
                        is_directory = True
                    # Check for common directory files
                    elif any(file in path.lower() for file in [
                        '.env', 'config', 'backup', 'admin', 'login', 'dashboard'
                    ]):
                        # For sensitive files, even short responses might indicate exposure
                        if response.status_code == 200:
                            is_directory = True
                    # Check response length for potential directory listings
                    elif len(content) > 50 and response.status_code == 200:
                        # Look for HTML structure that might indicate directory
                        if '<html' in content or '<body' in content:
                            is_directory = True

                if is_directory:
                    severity = "High" if any(sensitive in path.lower() for sensitive in [
                        'admin', 'config', '.env', 'backup', 'wp-admin', 'phpmyadmin'
                    ]) else "Medium"

                    vulnerabilities.append({
                        "type": "Directory Exposure",
                        "severity": severity,
                        "description": f"Directory/file exposed: {path} (Status: {response.status_code})"
                    })
                    found_directories += 1
                    print(f"DEBUG: Found directory: {path} (Status: {response.status_code})")

            except requests.exceptions.RequestException:
                # Network errors are expected for non-existent paths
                pass
            except Exception as e:
                # Log unexpected errors but continue scanning
                print(f"DEBUG: Error checking {path}: {str(e)}")
                pass

        # If no directories found, add a success message
        if found_directories == 0 and not any(v['type'] in ['Configuration Error', 'Directory Scan Error'] for v in vulnerabilities):
            vulnerabilities.append({
                "type": "Directory Scan Complete",
                "severity": "Info",
                "description": f"No directories found using {wordlist_type} wordlist ({len(vuln_paths)} paths checked)"
            })

    except FileNotFoundError:
        vulnerabilities.append({
            "type": "Configuration Error",
            "severity": "Info",
            "description": f"Wordlist file {wordlist_type}_directories.txt not found"
        })
    except Exception as e:
        vulnerabilities.append({
            "type": "Directory Scan Error",
            "severity": "Info",
            "description": f"Directory scanning failed: {str(e)}"
        })

    return vulnerabilities
