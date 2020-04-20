export class Player {
    player: String;
    pos: String;
    age: String;
    team: String;
    fgpercentage: Number;
    ftpercentage: Number;
    threep: Number;
    pts: Number;
    trb: Number;
    ast: Number;
    stl: Number;
    tov: Number;
    drafted: boolean;

}

export class Players {
    players: Array<Player>;
}

export class Inputs {
    leagueName: String;
    owner: String;
    teamName: String;
    categories: Number;
    leagueSize: Number;
    draftPos: Number;
    teamSize: Number;
    punt: String;
}