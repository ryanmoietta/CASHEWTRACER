#!/usr/bin/env python3

import os
import json
import socket
import datetime
import requests

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.prompt import Prompt


# =====================================================
# CASHEW TRACER
# Network Intelligence & IP Analysis Toolkit
# =====================================================


console = Console()

APP_NAME = "CASHEW TRACER"
VERSION = "1.0"

IP_API = "http://ip-api.com/json/"


# =====================================================
# UI
# =====================================================


def clear():
    os.system(
        "clear" if os.name == "posix"
        else "cls"
    )


def banner():

    logo = r"""

 ██████╗ █████╗ ███████╗██╗  ██╗███████╗██╗    ██╗
██╔════╝██╔══██╗██╔════╝██║  ██║██╔════╝██║    ██║
██║     ███████║███████╗███████║█████╗  ██║ █╗ ██║
██║     ██╔══██║╚════██║██╔══██║██╔══╝  ██║███╗██║
╚██████╗██║  ██║███████║██║  ██║███████╗╚███╔███╔╝
 ╚═════╝╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝╚══════╝ ╚══╝╚══╝


.___________..______          ___       ______  _______ .______      
|           ||   _  \        /   \     /      ||   ____||   _  \     
`---|  |----`|  |_)  |      /  ^  \   |  ,----'|  |__   |  |_)  |    
    |  |     |      /      /  /_\  \  |  |     |   __|  |      /     
    |  |     |  |\  \----./  _____  \ |  `----.|  |____ |  |\  \----.
    |__|     | _| `._____/__/     \__\ \______||_______|| _| `._____|
                                                                     

        Network Intelligence
        & IP Analysis Toolkit

    """

    console.print(
        Panel.fit(
            logo,
            title="[bold cyan]CASHEW TRACER[/bold cyan]",
            subtitle="[bold green]v1.0 ONLINE[/bold green]",
            border_style="cyan"
        )
    )



# =====================================================
# NETWORK INFORMATION
# =====================================================


def get_public_ip():

    try:

        return requests.get(
            "https://api.ipify.org",
            timeout=5
        ).text

    except:

        return "Unknown"



def get_private_ip():

    try:

        hostname = socket.gethostname()

        return socket.gethostbyname(hostname)

    except:

        return "Unknown"



def reverse_dns(ip):

    try:

        return socket.gethostbyaddr(ip)[0]

    except:

        return "Unavailable"



# =====================================================
# IP INTELLIGENCE
# =====================================================


def lookup_ip(ip):

    try:

        response = requests.get(
            IP_API + ip,
            timeout=5
        )

        return response.json()


    except Exception as error:

        return {
            "status": "fail",
            "message": str(error)
        }



def analyze_ip(ip):

    with Progress(
        SpinnerColumn(),
        TextColumn(
            "[cyan]Gathering intelligence..."
        )
    ) as progress:

        progress.add_task(
            "",
            total=None
        )

        data = lookup_ip(ip)



    if data.get("status") != "success":

        console.print(
            "[red]Lookup failed[/red]"
        )

        return None



    report = {

        "time":
        str(datetime.datetime.now()),


        "ip":
        ip,


        "hostname":
        socket.gethostname(),


        "reverse_dns":
        reverse_dns(ip),


        "country":
        data.get("country"),


        "region":
        data.get("regionName"),


        "city":
        data.get("city"),


        "timezone":
        data.get("timezone"),


        "latitude":
        data.get("lat"),


        "longitude":
        data.get("lon"),


        "isp":
        data.get("isp"),


        "organization":
        data.get("org"),


        "asn":
        data.get("as"),


    }


    return report



# =====================================================
# DISPLAY
# =====================================================


def show_report(report):

    table = Table(
        title="INTELLIGENCE REPORT",
        border_style="cyan"
    )


    table.add_column(
        "FIELD",
        style="green"
    )

    table.add_column(
        "VALUE",
        style="white"
    )


    for key,value in report.items():

        table.add_row(
            key.upper(),
            str(value)
        )


    console.print(table)



# =====================================================
# EXPORT
# =====================================================


def export_json(data):

    filename = (
        "cashew_report_"
        +
        datetime.datetime.now()
        .strftime("%Y%m%d_%H%M%S")
        +
        ".json"
    )


    with open(
        filename,
        "w"
    ) as file:

        json.dump(
            data,
            file,
            indent=4
        )


    console.print(
        f"[green]Saved:[/green] {filename}"
    )
# =====================================================
# WEBSITE INTELLIGENCE
# =====================================================


def website_to_ip():

    domain = Prompt.ask(
        "\n[cyan]Enter website/domain[/cyan]"
    )

    try:

        ip = socket.gethostbyname(domain)


        result = {

            "website":
            domain,

            "resolved_ip":
            ip,

            "reverse_dns":
            reverse_dns(ip)

        }


        console.print(
            Panel.fit(
                f"""
Website:
{domain}

IPv4:
{ip}

Reverse DNS:
{result['reverse_dns']}
                """,
                title="Website Intelligence",
                border_style="green"
            )
        )


        save = Prompt.ask(
            "Export report? y/n",
            default="n"
        )


        if save.lower() == "y":

            export_json(result)



    except Exception as error:

        console.print(
            f"[red]Failed:[/red] {error}"
        )



# =====================================================
# PHONE NUMBER INTELLIGENCE
# =====================================================


def phone_lookup():

    import phonenumbers

    from phonenumbers import (
        geocoder,
        carrier,
        timezone
    )


    number = Prompt.ask(
        "\n[cyan]Enter phone number (+countrycode)[/cyan]"
    )


    try:

        parsed = phonenumbers.parse(
            number,
            None
        )


        country = geocoder.description_for_number(
            parsed,
            "en"
        )


        service = carrier.name_for_number(
            parsed,
            "en"
        )


        zones = timezone.time_zones_for_number(
            parsed
        )


        result = {

            "number":
            number,


            "country":
            country,


            "carrier":
            service,


            "timezone":
            list(zones),


            "valid":
            phonenumbers.is_valid_number(parsed)

        }



        table = Table(
            title="PHONE INTELLIGENCE",
            border_style="cyan"
        )


        table.add_column(
            "FIELD",
            style="green"
        )


        table.add_column(
            "VALUE"
        )


        for k,v in result.items():

            table.add_row(
                k.upper(),
                str(v)
            )


        console.print(table)



    except Exception as error:

        console.print(
            f"[red]Invalid number:[/red] {error}"
        )



# =====================================================
# NETWORK DASHBOARD
# =====================================================


def my_network():


    console.print(
        "[cyan]Collecting local network data...[/cyan]"
    )


    public_ip = get_public_ip()

    private_ip = get_private_ip()



    report = analyze_ip(
        public_ip
    )


    if report:

        report["private_ip"] = private_ip


        show_report(
            report
        )


        export = Prompt.ask(
            "Export JSON? y/n",
            default="n"
        )


        if export.lower() == "y":

            export_json(
                report
            )



# =====================================================
# IP TRACE
# =====================================================


def trace_ip():

    ip = Prompt.ask(
        "\n[cyan]Target IP[/cyan]"
    )


    report = analyze_ip(
        ip
    )


    if report:

        show_report(
            report
        )


        export = Prompt.ask(
            "Export JSON? y/n",
            default="n"
        )


        if export.lower() == "y":

            export_json(
                report
            )



# =====================================================
# MENU
# =====================================================


def menu():

    while True:


        console.print(
            """
[bold cyan]
╔══════════════════════════════╗
║       CASHEW TRACER           ║
╚══════════════════════════════╝
[/bold cyan]


[green]1[/green]  Analyze My Network

[yellow]2[/yellow]  Trace IP Address

[blue]3[/blue]  Website → IP Extraction

[magenta]4[/magenta] Phone Number Intelligence

[red]5[/red]  Exit

"""
        )


        choice = Prompt.ask(
            "Select option"
        )



        if choice == "1":

            my_network()



        elif choice == "2":

            trace_ip()



        elif choice == "3":

            website_to_ip()



        elif choice == "4":

            phone_lookup()



        elif choice == "5":

            console.print(
                "[green]Closing CASHEW TRACER...[/green]"
            )

            break



        else:

            console.print(
                "[red]Invalid option[/red]"
            )



# =====================================================
# START
# =====================================================


if __name__ == "__main__":

    clear()

    banner()

    menu()
