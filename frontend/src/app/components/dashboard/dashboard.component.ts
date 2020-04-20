import { Component, OnInit, ElementRef, ViewChild} from '@angular/core';
import { NgForm } from '@angular/forms';
import { DashboardService } from '../../services/dashboard.service';
import { ActivatedRoute, Router } from '@angular/router';
import { Player, Players, Inputs } from '../../models/dashhboard';

@Component({
  selector: 'app-dashboard',
  templateUrl: './dashboard.component.html',
  styleUrls: ['./dashboard.component.css']
})
export class DashboardComponent implements OnInit {
  players: Array<Object> = [];
  results: Array<Object> = [];
  homeActive: boolean = true;
  resultsActive: boolean = false;
  myDraftActive: boolean = false;
  draftSheetActive: boolean = false;
  userActive: boolean = false;
  infoActive: boolean = false;
  @ViewChild("middleA") middleA: ElementRef;
  @ViewChild("middleB") middleB: ElementRef;
  @ViewChild("middleK") middleK: ElementRef;
  inputModel: Inputs = new Inputs();
  inputsSet: boolean = false;
  draftType: String = "mock";
  scoringFormat: String = "h2h";
  draftFormat: String = "snake";


  constructor(
    private dashboardService: DashboardService,
    private router: Router,
    private route: ActivatedRoute
  ) { }

  ngOnInit(): void {
    console.log("Loading page...");
    this.dashboardService.getPlayers().then(res => {
      for (let i = 0; i < res.length; ++i) {
        let player = {};
        player["index"] = i;
        player["player"] = res[i].PLAYER;
        player["pos"] = res[i].POS;
        player["age"] = res[i].AGE;
        player["team"] = res[i].TEAM;
        player["fg%"] = res[i]["FG%"];
        player["ft%"] = res[i]["FT%"];
        player["3P"] = res[i]["3P"];
        player["pts"] = res[i].PTS;
        player["trb"] = res[i].TRB;
        player["ast"] = res[i].AST;
        player["stl"] = res[i].STL;
        player["tov"] = res[i].TOV;
        player["drafted"] = res[i].DRAFTED;
        this.players.push(player);
      }
      console.log(this.players);
    });
  }

  getInput(inputForm: NgForm) {
    if (inputForm.invalid) {
      console.log("INVALID");
      return;
    }
    let data = {
      league_name: this.inputModel.leagueName, 
      owner_name: this.inputModel.owner,
      team_name: this.inputModel.teamName,
      draft_type: this.draftType,
      scoring_format: this.scoringFormat,
      cats: this.inputModel.categories,
      draft_format: this.draftFormat,
      league_size: this.inputModel.leagueSize,
      draft_pos: this.inputModel.draftPos,
      team_size: this.inputModel.teamSize,
      to_punt: this.inputModel.punt
    };
    this.dashboardService.getInput(data).then(res => {
      console.log(res);
      this.inputsSet = true;
      console.log(this.inputsSet);
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




  mouseoverAlexis(){
    this.middleA.nativeElement.style.opacity = "1";
  }

  mouseoutAlexis(){
    this.middleA.nativeElement.style.opacity = "0";
  }


  mouseoverBrennan(){
    this.middleB.nativeElement.style.opacity = "1";
  }

  mouseoutBrennan(){
    this.middleB.nativeElement.style.opacity = "0";
  }


  mouseoverKeara(){
    this.middleK.nativeElement.style.opacity = "1";
  }

  mouseoutKeara(){
    this.middleK.nativeElement.style.opacity = "0";
  }

  removePlayer(player) {
    this.players[player.index]["drafted"] = 1;
    this.results.push(player);
  }

}
