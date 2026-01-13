function Start-Project {
    Write-Host "`n Démarrage..." -ForegroundColor Cyan
    docker-compose up -d
    Write-Host " Démarré !`n" -ForegroundColor Green
}

function Stop-Project {
    Write-Host "`n Arrêt..." -ForegroundColor Yellow
    docker-compose down
    Write-Host " Arrêté !`n" -ForegroundColor Green
}

function Migrate-All {
    Write-Host "`n Migrations..." -ForegroundColor Cyan
    docker exec -it autodf-api-1 python manage.py makemigrations
    docker exec -it autodf-api-1 python manage.py migrate
    Write-Host " Terminé !`n" -ForegroundColor Green
}

function Create-SuperUser {
    Write-Host "`n SuperUser...`n" -ForegroundColor Cyan
    docker exec -it autodf-api-1 python manage.py createsuperuser
}

function Show-Logs {
    Write-Host "`n Logs...`n" -ForegroundColor Cyan
    docker logs autodf-api-1
}

function Enter-Container {
    Write-Host "`n Container...`n" -ForegroundColor Cyan
    docker exec -it autodf-api-1 bash
}

function Show-Commands {
    Write-Host "`n=== COMMANDES ===" -ForegroundColor Cyan
    Write-Host "Start-Project     - Démarre" -ForegroundColor Yellow
    Write-Host "Stop-Project      - Arrête" -ForegroundColor Yellow
    Write-Host "Migrate-All       - Migrations" -ForegroundColor Yellow
    Write-Host "Create-SuperUser  - Admin" -ForegroundColor Yellow
    Write-Host "Show-Logs         - Logs" -ForegroundColor Yellow
    Write-Host "Enter-Container   - Bash" -ForegroundColor Yellow
    Write-Host "Show-Commands     - Aide`n" -ForegroundColor Yellow
}

Write-Host "`n Scripts chargés !`n" -ForegroundColor Green
Show-Commands
