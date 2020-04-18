import { Component, OnInit, ElementRef, ViewChild} from '@angular/core';
import { DashboardService } from '../../services/dashboard.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Player, Players } from '../../models/dashhboard';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  players: Players = new Players();
  homeActive: boolean = true;
  resultsActive: boolean = false;
  myDraftActive: boolean = false;
  draftSheetActive: boolean = false;
  userActive: boolean = false;
  infoActive: boolean = false;
  @ViewChild("middle") middle: ElementRef;
  sticky: boolean = false;
  @ViewChild('stickyNav') navElement: ElementRef;
  navPositon: any;

  constructor(
    private dashboardService: DashboardService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    console.log("Loading page...");
    this.dashboardService.getPlayers().then(res => {
      console.log(res);
      this.players = res;
    });
  }

  getActive(value: string) {
    if (value === 'mydraft') {
      return this.myDraftActive ? 'navbar-active' : '';
    } else if (value === 'draftsheet') {
      return this.draftSheetActive ? 'navbar-active' : '';
    } else if (value === 'results') {
      return this.resultsActive ? 'navbar-active' : '';
    }
  }

  setActive(value: string) {
    if (value === 'mydraft') {
      this.myDraftActive = true;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.userActive = false;
      this.infoActive = false;
    } else if (value === 'draftsheet') {
      this.draftSheetActive = true;
      this.myDraftActive = false;
      this.resultsActive = false;
      this.homeActive = false;
      this.userActive = false;
      this.infoActive = false;
    } else if (value === 'results') {
      this.resultsActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.homeActive = false;
      this.userActive = false;
      this.infoActive = false;
    } else if (value === 'home') {
      this.homeActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.userActive = false;
      this.infoActive = false;
    } else if (value === 'user') {
      this.userActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.infoActive = false;
      this.homeActive = false;
    } else if(value === 'info') {
      this.infoActive = true;
      this.myDraftActive = false;
      this.draftSheetActive = false;
      this.resultsActive = false;
      this.userActive = false;
      this.homeActive = false;
    }
  }



ngAfterViewInit(){
    this.navPosition = this.navElement.nativeElement.offsetTop
}

//BROKEN PART
@HostListener('window:scroll', ['$event'])
    handleScroll(){
        const windowScroll = window.pageYOffset;
        if(windowScroll >= this.navPosition){
            this.sticky = true;
        } else {
            this.sticky = false;
        }
    }


 mouseoverAlexis(){
  this.middle.nativeElement.style.opacity = "1";
}

 mouseoutAlexis(){
  this.middle.nativeElement.style.opacity = "0";
}

}
