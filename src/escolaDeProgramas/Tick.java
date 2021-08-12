package escolaDeProgramas;

import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;

public class Tick implements ActionListener{
	private Tickavel escola;
	
	public Tick(Tickavel escola)
	{
		System.out.println("hohoho");
		this.escola = escola;
	}
	
	public void actionPerformed(ActionEvent ae) {
		this.escola.tick();
	}
}
