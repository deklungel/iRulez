import React, { Component }  from 'react';
import PersistentDrawerLeft from './SideBar';
import withAuth from './withAuth';

export default function withMenuList(MenuComponent) {
    return class ListWrapped extends Component {

    
        
    render() {
        return(
                  //<MenuComponent></MenuComponent>
           <div>
             <PersistentDrawerLeft maindata={withAuth(MenuComponent)} history={this.props.history}></PersistentDrawerLeft>
           </div>
        )
        ;
    }

    }
}
